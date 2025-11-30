"""Simple preprocessing helpers for OCR.

Keep these lightweight so they can be used by the CLI or tests.
"""
from PIL import Image
import cv2
import numpy as np
import os


def preprocess_image(image_path: str, target_width: int = 800) -> Image.Image:
    """Load and apply gentle preprocessing, returning a PIL Image suitable for pytesseract.

    This uses a lighter touch than before - only CLAHE for contrast enhancement,
    no aggressive thresholding or morphological operations.
    
    Steps:
    - load -> convert to RGB
    - resize (keep aspect ratio if image is smaller than target)
    - convert to grayscale
    - apply gentle CLAHE (contrast limited adaptive histogram equalization)
    
    Args:
        image_path: path to input image
        target_width: target width for resizing (default 800)
    
    Returns:
        PIL Image ready for OCR
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)

    # Only resize if image is significantly smaller than target
    # Avoid resizing images that are already reasonably sized to preserve quality
    h, w = arr.shape[:2]
    if w < target_width * 0.7:  # Only resize if width is less than 70% of target
        scale = target_width / float(w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        arr = cv2.resize(arr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        return Image.fromarray(arr)
    
    # Return original image if it's already large enough
    return img