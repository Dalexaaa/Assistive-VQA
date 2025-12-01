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
        # Try multiple PSM modes and pick longest result
        results = []
        
        # PSM 3 (automatic - default)
        try:
            ocr3 = OCR(psm=3)
            text3 = ocr3.extract_text(image_path)
            results.append(text3)
        except Exception as e:
            print(f"[OCR] PSM 3 failed: {e}")
        
        # PSM 11 (sparse text - good for signs)
        try:
            ocr11 = OCR(psm=11)
            text11 = ocr11.extract_text(image_path)
            results.append(text11)
        except Exception as e:
            print(f"[OCR] PSM 11 failed: {e}")
        
        # PSM 6 (single block - good for structured text)
        try:
            ocr6 = OCR(psm=6)
            text6 = ocr6.extract_text(image_path)
            results.append(text6)
        except Exception as e:
            print(f"[OCR] PSM 6 failed: {e}")
        
        if not results:
            return "No text found"
        
        # Pick the longest result
        raw_text = max(results, key=lambda x: len(x.replace('\n', ' ').strip()))
        
        # Apply spell correction and normalization
        corrected_text = normalize_ocr(raw_text)
        
        return corrected_text if corrected_text else "No text found"
        
    except Exception as e:
        import traceback
        return f"OCR Error: {str(e)}\n{traceback.format_exc()}"


if __name__ == "__main__":
    # Command line usage
    if len(sys.argv) > 1:
        test_text = extract_text(sys.argv[1])
        print(test_text)
    else:
        print("Usage: python ocr_module.py <image_path>")
