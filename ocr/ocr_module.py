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
        
        # Try multiple PSM modes and combine results
        results = []
        
        # PSM 3 (automatic - default)
        raw_text = ocr_engine.perform_ocr(preprocessed)
        results.append(raw_text)
        
        # PSM 11 (sparse text - good for signs)
        try:
            psm11_ocr = OCR(psm=11)
            psm11_text = psm11_ocr.perform_ocr(preprocessed)
            results.append(psm11_text)
        except:
            pass
        
        # PSM 6 (single block - good for structured text)
        try:
            psm6_ocr = OCR(psm=6)
            psm6_text = psm6_ocr.perform_ocr(preprocessed)
            results.append(psm6_text)
        except:
            pass
        
        # Pick the result with most actual words (longest after stripping whitespace)
        raw_text = max(results, key=lambda x: len(x.replace('\n', ' ').strip())) if results else raw_text
        
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
