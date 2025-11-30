"""
Test script for OCR functionality.

Compares the output of the main OCR pipeline (extract_text) with
the raw OCR output (perform_ocr) to verify improvements.
"""

import sys
import os

# Add the ocr-app source to path
ocr_app_src = os.path.join(os.path.dirname(__file__), "ocr-app", "src")
if ocr_app_src not in sys.path:
    sys.path.insert(0, ocr_app_src)

from ocr_module import extract_text
from ocr_app.ocr import OCR
from PIL import Image


def test_ocr(image_path):
    """Test OCR on a single image."""
    print(f"Testing OCR on: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    print("-" * 20)
    print("Result from ocr_module.extract_text (RECOMMENDED):")
    try:
        text = extract_text(image_path)
        print(text)
    except Exception as e:
        print(f"Error: {e}")
        
    print("-" * 20)
    print("Result from ocr_app.ocr.OCR().perform_ocr (RAW):")
    try:
        ocr = OCR()
        img = Image.open(image_path).convert("RGB")
        text = ocr.perform_ocr(img)
        print(text)
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)


if __name__ == "__main__":
    # Test images
    images = ["image1.jpg", "image2.jpg", "image3.jpg"]
    
    for img_name in images:
        print(f"\n{'='*40}")
        print(f"Testing {img_name}")
        print(f"{'='*40}")
        image_path = os.path.join(os.path.dirname(__file__), "ocr-app", img_name)
        test_ocr(image_path)
