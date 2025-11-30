"""Configuration container for OCR defaults."""
from dataclasses import dataclass


@dataclass
class Config:
    tesseract_cmd: str | None = None
    lang: str = "eng"
    oem: int = 3
    psm: int = 3
# Configuration settings for the OCR application

# File paths
IMAGE_PATH = "path/to/images/"
OUTPUT_PATH = "path/to/output/"
MODEL_PATH = "path/to/model/"

# OCR settings
TESSERACT_CMD = "tesseract"  # Command to run Tesseract OCR
LANGUAGE = "eng"  # Default language for OCR

# Preprocessing settings
IMAGE_SIZE = (1024, 768)  # Default size for resizing images
GRAYSCALE = True  # Whether to convert images to grayscale

# Logging settings
LOG_LEVEL = "INFO"  # Default logging level
LOG_FILE = "ocr_app.log"  # Log file name

# Other constants
MAX_RETRIES = 3  # Maximum number of retries for OCR processing