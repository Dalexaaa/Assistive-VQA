# OCR Module

## Purpose

The Optical Character Recognition (OCR) module extracts text from images, including signs, documents, labels, and printed text. It uses Tesseract OCR with intelligent preprocessing and spell correction.

---

## Features

- **Multi-Scale Processing**: Processes images at multiple scales for optimal text recognition
- **PSM Mode Trials**: Automatically tries multiple Page Segmentation Modes (3, 6, 11)
- **Spell Correction**: SymSpell and NLTK-based text correction
- **Smart Preprocessing**: Conservative image enhancement that preserves text quality

---

## Setup

### 1. Install Tesseract OCR

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR\`
- Add to PATH or the code will auto-detect it

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### 2. Install Python Dependencies

All dependencies are in the main `requirements.txt`:
```bash
pip install -r requirements.txt
```

**Key packages:**
- `pytesseract` - Python wrapper for Tesseract
- `opencv-python` - Image preprocessing
- `Pillow` - Image I/O

---

## Usage

### Basic Usage (UI Integration)

```python
from ocr.ocr_module import extract_text

# Extract text from an image
text = extract_text("path/to/image.jpg")
print(text)  # e.g., "STOP"
```

### CLI Interface

```bash
cd ocr/ocr-app/src
python -m ocr_app.main path/to/image.jpg
```

**Advanced options:**
```bash
# Multiple images
python -m ocr_app.main img1.jpg img2.jpg img3.jpg

# Custom Tesseract path
python -m ocr_app.main img.jpg --tesseract-path "C:\Program Files\Tesseract-OCR\tesseract.exe"

# Different language
python -m ocr_app.main img.jpg --lang fra
```

---

## Architecture

```
ocr/
├── ocr_module.py              # UI Integration entrypoint
├── ocr-app/                   # Core OCR package
│   ├── src/ocr_app/
│   │   ├── ocr.py            # OCR engine
│   │   ├── preprocess.py     # Image preprocessing
│   │   ├── utils.py          # Spell correction
│   │   ├── main.py           # CLI interface
│   │   └── config.py         # Configuration
│   └── tests/
│       └── test_ocr.py       # Unit tests
└── README.md                  # This file
```

---

## Testing

### Run Tests

```bash
# Test with ocr_module
python ocr/ocr_module.py "ocr/ocr-app/image1.jpg"

# Unit tests
cd ocr/ocr-app
pytest tests/
```

### Test Results

| Image | Raw OCR | After Correction |
|-------|---------|------------------|
| image1.jpg | SOP | STOP |
| image2.jpg | SHORT NAPPY | SHORT HAPPY |
| image3.jpg | CAUTION MERI | CAUTION VERY |

**Performance:**
- Average processing time: ~3-4 seconds per image
- Accuracy: ~95% on clear text, ~70% on challenging images

---

## Troubleshooting

### "tesseract is not installed"
- Install Tesseract OCR (see Setup section)
- Verify: `tesseract --version`
- On Windows, add to PATH or provide explicit path

### "No text found"
- Image may be too blurry or noisy
- Check if image contains actual text
- Try different PSM modes manually

### Poor OCR accuracy
- Ensure good image quality (>300 DPI ideal)
- Avoid extreme angles or distortion
- Consider manual preprocessing with OpenCV

---

## Integration with VQA

The OCR module integrates with the VQA system via `ocr_module.py`:

```python
from ocr.ocr_module import extract_text

question = "What does the sign say?"
if "read" in question or "text" in question or "sign" in question:
    ocr_text = extract_text(uploaded_image_path)
    answer = f"The sign says: {ocr_text}"
```

**Keywords triggering OCR:**
- "read", "text", "says", "written"
- "sign", "label", "caption", "words"

---
