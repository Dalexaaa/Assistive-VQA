# ...existing code...
from PIL import Image
import pytesseract
import cv2
import numpy as np
import os
import shutil
import platform


_COMMON_WINDOWS_TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
]

class OCR:
    def __init__(self, tesseract_cmd: str = None, lang: str = "eng", oem: int = 3, psm: int = 3):
        """
        tesseract_cmd: full path to tesseract.exe on Windows (optional).
        lang: language code for Tesseract.
        oem, psm: Tesseract engine/mode config.
        """
        # allow explicit override
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            # try to detect tesseract on PATH
            which = shutil.which("tesseract")
            if which:
                pytesseract.pytesseract.tesseract_cmd = which
            else:
                # on Windows, try common install locations
                if platform.system().lower().startswith("win"):
                    for p in _COMMON_WINDOWS_TESSERACT_PATHS:
                        if os.path.isfile(p):
                            pytesseract.pytesseract.tesseract_cmd = p
                            break

        # verify availability early with a helpful error
        try:
            # this raises if tesseract is not found or broken
            _ = pytesseract.get_tesseract_version()
        except Exception as exc:
            msg = (
                "tesseract is not installed or it's not in your PATH. "
                "Install Tesseract and/or provide its full path via the `tesseract_cmd` argument or the CLI flag `--tesseract-path`. "
                "On Windows, install from https://github.com/UB-Mannheim/tesseract/wiki and add the install folder to your PATH."
            )
            raise RuntimeError(msg) from exc
        self.lang = lang
        self.config = f"--oem {oem} --psm {psm}"

    def load_image(self, image_path: str) -> Image.Image:
        """Load an image from the specified path and return a PIL Image (RGB)."""
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return Image.open(image_path).convert("RGB")

    def perform_ocr(self, image: Image.Image) -> str:
        """Perform OCR on the given PIL Image and return extracted text."""
        # convert to numpy + grayscale
        arr = np.array(image)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

        # denoise and enhance
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        # adaptive threshold to improve contrast for OCR
        th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

        pil_for_ocr = Image.fromarray(th)

        text = pytesseract.image_to_string(pil_for_ocr, lang=self.lang, config=self.config)
        return text.strip()

    def extract_text(self, image_path: str) -> str:
        """Load an image and extract text from it."""
        image = self.load_image(image_path)
        return self.perform_ocr(image)
# ...existing code...