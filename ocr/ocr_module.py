"""
OCR Module - Optical Character Recognition
Integrates the OCR implementation with the UI.
"""

import sys
import os
from PIL import Image

# Add the ocr-app source to path
ocr_app_src = os.path.join(os.path.dirname(__file__), "ocr-app", "src")
if ocr_app_src not in sys.path:
    sys.path.insert(0, ocr_app_src)

from ocr_app.ocr import OCR
from ocr_app.preprocess import preprocess_image
from ocr_app.utils import normalize_ocr


def extract_text(image_path):
    """
    Extract text from an image using OCR with advanced preprocessing and spell correction.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: The extracted text from the image
    """
    try:
        # Initialize OCR engine
        ocr_engine = OCR()
        
        # Preprocess the image
        try:
            preprocessed = preprocess_image(image_path)
        except Exception as e:
            print(f"[OCR] Preprocessing failed, using direct load: {e}")
            preprocessed = Image.open(image_path).convert("RGB")
        
        # Use the new confidence-based multi-PSM method
        raw_text, confidence = ocr_engine.ocr_with_best_psm(preprocessed)
        
        # Apply spell correction and normalization
        corrected_text = normalize_ocr(raw_text)
        
        return corrected_text if corrected_text else "No text found"
        
    except Exception as e:
        return f"OCR Error: {str(e)}"


if __name__ == "__main__":
    # Command line usage
    if len(sys.argv) > 1:
        test_text = extract_text(sys.argv[1])
        print(test_text)
    else:
        print("Usage: python ocr_module.py <image_path>")
