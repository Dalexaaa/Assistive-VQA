"""
Debug script for OCR pipeline inspection.

This script helps diagnose OCR accuracy issues by showing:
- Preprocessing results
- Raw OCR output for different PSM modes
- Confidence scores
- Normalized text output
"""

import sys
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Add the ocr-app source to path
ocr_app_src = os.path.join(os.path.dirname(__file__), "ocr-app", "src")
if ocr_app_src not in sys.path:
    sys.path.insert(0, ocr_app_src)

from ocr_app.ocr import OCR
from ocr_app.preprocess import preprocess_image
from ocr_app.utils import normalize_ocr


def debug_ocr(image_path):
    """Debug OCR pipeline for a given image."""
    print(f"Debugging OCR on: {image_path}")
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    ocr = OCR()
    
    # 1. Preprocessing
    print("\n--- Preprocessing ---")
    try:
        preprocessed = preprocess_image(image_path)
        print(f"Preprocessed image size: {preprocessed.size}")
        debug_save_path = image_path + ".debug_preprocessed.jpg"
        preprocessed.save(debug_save_path)
        print(f"Saved preprocessed image to: {debug_save_path}")
    except Exception as e:
        print(f"Preprocessing failed: {e}")
        preprocessed = Image.open(image_path).convert("RGB")

    # 2. Apply thresholding (same as OCR pipeline)
    print("\n--- Raw OCR Results (No Normalization) ---")
    arr = np.array(preprocessed)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, 11, 2)
    pil_img = Image.fromarray(th)
    
    # Save thresholded image
    th_save_path = image_path + ".debug_thresholded.jpg"
    pil_img.save(th_save_path)
    print(f"Saved thresholded image to: {th_save_path}")

    # 3. Test different PSM modes
    psm_modes = [3, 6, 11, 13]
    for psm in psm_modes:
        print(f"\nTesting PSM {psm}:")
        config = f"--oem 3 --psm {psm}"
        try:
            # Get confidence data
            data = pytesseract.image_to_data(pil_img, lang='eng', 
                                            config=config, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf, text in zip(data['conf'], data['text']) 
                          if conf != '-1' and text.strip()]
            
            # Replicate scoring logic from ocr.py
            valid_confidences = [c for c in confidences if c > 30]
            score = sum(valid_confidences)
            
            # Get text
            text = pytesseract.image_to_string(pil_img, lang='eng', config=config)
            text = text.strip()
            
            # Apply penalties
            if len(text) < 3:
                score *= 0.5
            
            print(f"  Raw Text: '{text}'")
            print(f"  Confidences: {confidences}")
            print(f"  Valid Confidences (>30): {valid_confidences}")
            print(f"  Calculated Score: {score:.2f}")
            print(f"  Normalized: '{normalize_ocr(text)}'")
        except Exception as e:
            print(f"  Failed: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Default to image1.jpg for debugging
        image_path = os.path.join(os.path.dirname(__file__), "ocr-app", "image1.jpg")
    
    debug_ocr(image_path)
