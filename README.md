# Assistive-VQA (SEA710 Project)
This project aims to create an assistive system that can answer visual questions about images,
helping visually impaired users understand their surroundings.

---

## Team Members

| Role | Member | Description |
|------|---------|-------------|
| Person 1 | Abby | VQA + Repository Setup |
| Person 2 | Rajini | UI + Integration of VQA and OCR |
| Person 3 | TBD | OCR + Final Presentation and Demo |

---

## Project Overview

The system combines three main modules:
1. **VQA (Visual Question Answering)** – Interprets questions and answers about visual content using models like BLIP-2 or LLaVA.  
2. **OCR (Optical Character Recognition)** – Reads and extracts text from images using Tesseract and image preprocessing.  
3. **UI + Integration** – Provides an interface for users to upload or capture images and ask questions.

The final prototype will:
- Accept an image and a question.
- Determine whether to use OCR or VQA.
- Display the answer.
- Serve as an assistive tool for visually impaired users.

---

## Repository Structure

```
assistive-vqa/
│
├── vqa/                  ← VQA model (BLIP-2 / LLaVA)
│   └── README.md
│
├── ocr/                  ← OCR module (Tesseract + preprocessing)
│   └── README.md
│
├── ui/                   ← User interface + Integration
│   └── README.md
│
├── data/
│   ├── samples/          ← Example images
│   └── cases.csv         ← Test cases (image, question, type)
│
├── docs/
│   └── eval.md
│
├── requirements.txt      ← Common dependencies
├── main.py               ← Entry point for final system
├── .gitignore
└── README.md
```

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dalexaaa/Assistive-VQA.git
cd Assistive-VQA
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
---

## Usage

1. Run the complete system:
```bash
python main.py
```

2. Or test each module individually:
```bash
python vqa/vqa_model.py
python ocr/ocr_module.py
```

# Testing
Each member must:
- Provide 3–5 test examples in their own folder (/vqa, /ocr, /ui).
- Update the /data/samples/ directory with shared test images.
- Document results and examples in their module’s README.

# Integration
Integration happens in two layers:
- route(question) decides whether to use OCR or VQA.
- main.py or app.py connects both and displays the response through the UI.

# Evaluation
A simple evaluation is included in /docs/eval.md:
- 10 total test cases (mix of text and visual questions)
- Latency, accuracy, and clarity of results

## Folder Responsabilities
Each folder has its own README.md with:
* Purpose of the module
* Setup & usage instructions
* Examples and screenshots

---

