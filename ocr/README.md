# OCR Module

**Owner:** Person 3  
**Status:** To be implemented

## Purpose

The Optical Character Recognition (OCR) module extracts and reads text from images, including signs, documents, labels, and handwritten text.

## Requirements

This module should implement the `extract_text()` function that will be called by the integration layer.

## Interface

```python
def extract_text(image_path: str) -> str:
    """
    Extract text from an image using OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: The extracted text from the image
    """
    # Your implementation here
    pass
```

## Suggested Implementation

### Recommended Approach
- **Tesseract OCR** for text extraction
- **OpenCV** for image preprocessing
- **PIL/Pillow** for image handling

### Example Implementation

```python
import pytesseract
from PIL import Image
import cv2
import numpy as np

def extract_text(image_path: str) -> str:
    # Load image
    image = Image.open(image_path)
    
    # Convert to OpenCV format for preprocessing
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Preprocessing for better OCR
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Optional: noise removal
    # gray = cv2.medianBlur(gray, 3)
    
    # Extract text
    text = pytesseract.image_to_string(gray)
    
    # Clean up the text
    text = text.strip()
    
    return text if text else "No text found in the image."
```

## Setup Instructions

### 1. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

### 2. Install Python Dependencies

```bash
pip install pytesseract opencv-python pillow
```

### 3. Implement the Function

Edit `ocr/ocr_module.py` with your implementation.

### 4. Test Independently

```bash
python ocr/ocr_module.py
```

## Example Usage

```python
from ocr.ocr_module import extract_text

# Test with different images
text = extract_text("sign.jpg")
print(text)  # Expected: "STOP" or sign text

text = extract_text("business_card.jpg")
print(text)  # Expected: contact information

text = extract_text("document.jpg")
print(text)  # Expected: document text
```

## Image Preprocessing Tips

For better OCR accuracy, try these preprocessing techniques:

```python
# 1. Grayscale conversion
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. Noise removal
denoised = cv2.fastNlMeansDenoising(gray)

# 3. Thresholding
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 4. Dilation and erosion
kernel = np.ones((1, 1), np.uint8)
dilated = cv2.dilate(thresh, kernel, iterations=1)
eroded = cv2.erode(dilated, kernel, iterations=1)

# 5. Resizing for small text
scaled = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
```

## Test Cases

Create test examples in this directory with:
- Sample images (signs, documents, menus)
- Expected extracted text
- Actual results
- Preprocessing methods used

## Integration

Your module will be automatically called by the UI when:
- Questions are about reading text
- Questions contain keywords like: "read", "text", "says", "written", "sign", "label"

No changes needed to integration code - just implement the function!

## Dependencies to Add

Add to `requirements.txt`:
```
pytesseract>=0.3.10
opencv-python>=4.8.1
```

## Configuration

You can configure Tesseract for better results:

```python
# Custom configuration
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(image, config=custom_config)

# PSM modes:
# 3 = Fully automatic page segmentation (default)
# 6 = Assume a single uniform block of text
# 7 = Treat the image as a single text line
# 11 = Sparse text. Find as much text as possible
```

## Resources

- [Tesseract Documentation](https://tesseract-ocr.github.io/)
- [pytesseract GitHub](https://github.com/madmaze/pytesseract)
- [OpenCV Tutorials](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [Image Preprocessing Guide](https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html)
