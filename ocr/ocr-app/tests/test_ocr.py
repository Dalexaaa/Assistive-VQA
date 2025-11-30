import unittest
from src.ocr_app.ocr import OCR

class TestOCR(unittest.TestCase):

    def setUp(self):
        self.ocr = OCR()

    def test_load_image(self):
        image_path = 'path/to/test/image.png'
        result = self.ocr.load_image(image_path)
        self.assertIsNotNone(result)

    def test_perform_ocr(self):
        image_path = 'path/to/test/image.png'
        self.ocr.load_image(image_path)
        extracted_text = self.ocr.perform_ocr()
        self.assertIsInstance(extracted_text, str)

    def test_preprocess_image(self):
        image_path = 'path/to/test/image.png'
        preprocessed_image = self.ocr.preprocess_image(image_path)
        self.assertIsNotNone(preprocessed_image)

if __name__ == '__main__':
    unittest.main()