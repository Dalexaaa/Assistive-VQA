# OCR Application

This project is an Optical Character Recognition (OCR) application that utilizes various libraries to extract text from images. The application is designed to preprocess images, perform OCR, and provide utility functions for enhanced functionality.

## Project Structure

```
ocr-app
├── src
│   └── ocr_app
│       ├── __init__.py
│       ├── main.py
│       ├── ocr.py
│       ├── preprocess.py
│       ├── config.py
│       └── utils.py
├── tests
│   ├── __init__.py
│   └── test_ocr.py
├── models
│   └── .gitkeep
├── notebooks
│   └── exploration.ipynb
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To run the OCR application, execute the following command:

```
python src/ocr_app/main.py [options]
```

## Features

- Image preprocessing to enhance text recognition.
- OCR functionality using Tesseract.
- Utility functions for logging and error handling.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.