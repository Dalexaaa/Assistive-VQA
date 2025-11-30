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
    
    def full_ocr(self, image: Image.Image, scales: tuple = (1.0, 1.5, 2.0)) -> str:
        """Perform multi-scale OCR with confidence tracking.
        
        Args:
            image: PIL Image to process
            scales: tuple of scaling factors to try
        
        Returns:
            Best extracted text across all scales
        """
        self.last_confidence = 0
        best_text = ""
        best_conf = 0
        
        for scale in scales:
            if scale != 1.0:
                w, h = image.size
                scaled = image.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
            else:
                scaled = image
            
            # Get text with confidence
            arr = np.array(scaled)
            gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray, h=10)
            th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
            
            # Get detailed data with confidence
            data = pytesseract.image_to_data(Image.fromarray(th), lang=self.lang, 
                                            config=self.config, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence for valid text
            confidences = [int(conf) for conf, text in zip(data['conf'], data['text']) 
                          if conf != '-1' and text.strip()]
            avg_conf = sum(confidences) / len(confidences) if confidences else 0
            
            # Get text
            text = pytesseract.image_to_string(Image.fromarray(th), lang=self.lang, config=self.config)
            text = text.strip()
            
            if avg_conf > best_conf and len(text) > len(best_text) * 0.5:
                best_conf = avg_conf
                best_text = text
        
        self.last_confidence = best_conf
        return best_text
    
    def _ocr_with_psm_trials(self, image: Image.Image) -> tuple:
        """Try different PSM modes and return best result with confidence.
        
        Args:
            image: PIL Image to process
        
        Returns:
            tuple: (best_text, best_confidence)
        """
        psm_modes = [3, 6, 11, 13]  # Different page segmentation modes
        best_text = ""
        best_conf = 0
        
        arr = np.array(image)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
        pil_img = Image.fromarray(th)
        
        for psm in psm_modes:
            config = f"--oem 3 --psm {psm}"
            try:
                data = pytesseract.image_to_data(pil_img, lang=self.lang, 
                                                config=config, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf, text in zip(data['conf'], data['text']) 
                              if conf != '-1' and text.strip()]
                avg_conf = sum(confidences) / len(confidences) if confidences else 0
                
                text = pytesseract.image_to_string(pil_img, lang=self.lang, config=config)
                text = text.strip()
                
                if avg_conf > best_conf and text:
                    best_conf = avg_conf
                    best_text = text
            except Exception:
                continue
        
        return best_text, best_conf
    
    def _detect_text_regions_mser(self, image: Image.Image) -> list:
        """Detect text regions using MSER (Maximally Stable Extremal Regions).
        
        Args:
            image: PIL Image to process
        
        Returns:
            list: Bounding boxes [(x, y, w, h), ...]
        """
        arr = np.array(image)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        
        # MSER detector
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        
        # Convert regions to bounding boxes
        boxes = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region)
            # Filter out very small or very large regions
            if 10 < w < gray.shape[1] * 0.8 and 10 < h < gray.shape[0] * 0.8:
                boxes.append((x, y, w, h))
        
        # Merge overlapping boxes
        if boxes:
            boxes = self._merge_boxes(boxes)
        
        return boxes
    
    def _merge_boxes(self, boxes: list) -> list:
        """Merge overlapping bounding boxes.
        
        Args:
            boxes: list of (x, y, w, h) tuples
        
        Returns:
            list: merged boxes
        """
        if not boxes:
            return []
        
        # Sort by x coordinate
        boxes = sorted(boxes, key=lambda b: b[0])
        merged = [boxes[0]]
        
        for current in boxes[1:]:
            last = merged[-1]
            # Check for overlap
            if current[0] <= last[0] + last[2]:
                # Merge boxes
                x = min(last[0], current[0])
                y = min(last[1], current[1])
                w = max(last[0] + last[2], current[0] + current[2]) - x
                h = max(last[1] + last[3], current[1] + current[3]) - y
                merged[-1] = (x, y, w, h)
            else:
                merged.append(current)
        
        return merged
    
    def _ocr_regions_and_merge(self, image: Image.Image, boxes: list) -> str:
        """Perform OCR on detected regions and merge results.
        
        Args:
            image: PIL Image to process
            boxes: list of (x, y, w, h) bounding boxes
        
        Returns:
            str: merged text from all regions
        """
        arr = np.array(image)
        texts = []
        
        for x, y, w, h in boxes:
            # Extract region
            region = arr[y:y+h, x:x+w]
            if region.size == 0:
                continue
            
            # Preprocess region
            gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray, h=10)
            th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
            
            # OCR on region
            text = pytesseract.image_to_string(Image.fromarray(th), 
                                              lang=self.lang, config=self.config)
            text = text.strip()
            if text:
                texts.append(text)
        
        return " ".join(texts)
# ...existing code...