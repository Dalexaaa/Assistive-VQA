"""Simple preprocessing helpers for OCR.

Keep these lightweight so they can be used by the CLI or tests.
"""
from PIL import Image
import cv2
import numpy as np
import os


def preprocess_image(image_path: str, target_width: int = 800) -> Image.Image:
    """Load and apply improved preprocessing, returning a PIL Image suitable for pytesseract.

    Steps:
    - load -> convert to RGB
    - resize (keep aspect)
    - convert to grayscale
    - denoise with bilateral filter
    - apply CLAHE (contrast limited adaptive histogram equalization)
    - adaptive threshold
    - morphological closing + dilation to strengthen broken strokes

    The pipeline is tuned to improve recognition on high-contrast signs like STOP.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)

    # resize preserving aspect ratio
    h, w = arr.shape[:2]
    if w < target_width:
        scale = target_width / float(w)
        new_w = int(w * scale)
        new_h = int(h * scale)
        arr = cv2.resize(arr, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    # preserve edges while denoising
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)

    # CLAHE for local contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    # adaptive threshold to get binary image
    th = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 4)

    # morphological operations to close gaps in letters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)
    dilated = cv2.dilate(closed, kernel, iterations=1)

    return Image.fromarray(dilated)
def resize_image(image, width, height):
    # Function to resize the image to the specified width and height
    pass

def convert_to_grayscale(image):
    # Function to convert the image to grayscale
    pass

def apply_filter(image):
    # Function to apply filters to enhance text recognition
    pass

def preprocess_image(image, width, height):
    # Function to preprocess the image before OCR
    image = resize_image(image, width, height)
    image = convert_to_grayscale(image)
    image = apply_filter(image)
    return image