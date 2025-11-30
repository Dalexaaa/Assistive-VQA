# OCR Module

Advanced OCR (Optical Character Recognition) system with confidence-based selection, preprocessing, and spell correction.

## Features

**Confidence-Based PSM Selection**: Automatically tries multiple Page Segmentation Modes (PSM) and selects the best result based on confidence scores  
**Image Preprocessing**: CLAHE enhancement and gentle preprocessing to improve OCR accuracy  
**Spell Correction**: Intelligent normalization using SymSpell and NLTK dictionaries  
**Noise Filtering**: Removes pure punctuation tokens and very short fragments  
**Multiple PSM Support**: Tests PSM modes 3, 6, 11, and 13 for optimal results

## Installation

### Prerequisites

1. **Tesseract OCR** must be installed on your system:
   - **Windows**: Download from [GitHub Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

2. **Python Dependencies**:
```bash
pip install -r ocr/ocr-app/requirements.txt
```

Required packages:
- `pytesseract` - Python wrapper for Tesseract
- `opencv-python` - Image processing
- `pillow` - Image handling
- `numpy` - Numerical operations
- `symspellpy` - Spell correction
- `nltk` - Natural language processing

## Usage

### Basic Usage (Recommended)

```python
from ocr_module import extract_text

# Extract text from an image
text = extract_text("path/to/image.jpg")
print(text)
```

**Example outputs:**
- `image1.jpg` → `"STOP"`
- `image2.jpg` → `"SHORT FUNNY HAPPY BIRTHDAY WISHES ROUTINELYSHARES.COM"`
- `image3.jpg` → `"CAUTION VERY TALKATIVE"`

### Advanced Usage

#### Get confidence scores:
```python
from ocr_app.ocr import OCR
from ocr_app.preprocess import preprocess_image

ocr = OCR()
preprocessed = preprocess_image("path/to/image.jpg")
text, confidence_score = ocr.ocr_with_best_psm(preprocessed)
print(f"Text: {text}, Score: {confidence_score}")
```

#### Raw OCR without normalization:
```python
from ocr_app.ocr import OCR
from PIL import Image

ocr = OCR()
img = Image.open("path/to/image.jpg").convert("RGB")
raw_text = ocr.perform_ocr(img)
print(raw_text)
```

## Testing

### Run all tests:
```bash
python ocr/reproduce_ocr.py
```

### Debug a specific image:
```bash
python ocr/debug_ocr.py path/to/image.jpg
```

The debug script will:
- Show preprocessing results
- Test all PSM modes
- Display confidence scores
- Save debug images (preprocessed and thresholded)

## Architecture

```
ocr/
├── ocr_module.py           # Main entry point (use extract_text)
├── reproduce_ocr.py        # Test script
├── debug_ocr.py           # Debug script
└── ocr-app/
    ├── src/ocr_app/
    │   ├── ocr.py         # Core OCR logic with PSM selection
    │   ├── preprocess.py  # Image preprocessing
    │   └── utils.py       # Normalization and spell correction
    └── requirements.txt   # Dependencies
```

## How It Works

1. **Preprocessing**: Images are resized and enhanced using CLAHE
2. **PSM Selection**: Tests multiple Page Segmentation Modes (3, 6, 11, 13)
3. **Scoring**: Each PSM result is scored based on:
   - Sum of confidence scores > 30
   - Penalty for non-alphanumeric text
   - Penalty for very short text
   - Bonus for word count
4. **Normalization**: Best result is cleaned up:
   - Explicit corrections (e.g., "SOP" → "STOP")
   - Punctuation filtering
   - Spell correction with SymSpell/NLTK

## Known Limitations

- **Low-quality images**: Very blurry or low-resolution images may produce poor results
- **Complex layouts**: Works best with simple text layouts (signs, labels, etc.)
- **Handwriting**: Not optimized for handwritten text

## API Reference

### `ocr_module.extract_text(image_path: str) -> str`
Main function for OCR. Returns cleaned, normalized text.

**Parameters:**
- `image_path`: Path to the image file

**Returns:**
- Extracted and normalized text as a string

### `OCR.ocr_with_best_psm(image: PIL.Image) -> tuple[str, float]`
Advanced OCR with confidence-based PSM selection.

**Parameters:**
- `image`: PIL Image object (preprocessed)

**Returns:**
- Tuple of (text, confidence_score)

### `OCR.perform_ocr(image: PIL.Image) -> str`
Basic OCR without PSM selection or normalization.

**Parameters:**
- `image`: PIL Image object

**Returns:**
- Raw OCR text

## Contributing

When making changes:
1. Test with `python ocr/reproduce_ocr.py`
2. Debug issues with `python ocr/debug_ocr.py path/to/problem_image.jpg`
3. Ensure all test images still produce correct output

