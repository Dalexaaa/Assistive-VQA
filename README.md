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

## Quick Start

### Option 1: Run Everything with One Command

```bash
./run-dev.sh
```

This will start both the Flask backend (port 5000) and Next.js frontend (port 3000).

### Option 2: Run Manually

**Terminal 1 - Backend:**
```bash
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd ui-webapp
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser!

---

## Repository Structure

```
assistive-vqa/
│
├── vqa/                  ← VQA model (BLIP-2 / LLaVA)
│   ├── vqa_model.py      ← Implement answer_question() here
│   └── README.md         ← Implementation guide
│
├── ocr/                  ← OCR module (Tesseract + preprocessing)
│   ├── ocr_module.py     ← Implement extract_text() here
│   └── README.md         ← Implementation guide
│
├── ui/                   ← Flask API backend
│   ├── app.py            ← Backend API (✅ Complete)
│   ├── README.md         ← Full documentation
│   ├── QUICK_START.md    ← Quick setup guide
│   └── tests/            ← Test cases and results
│
├── ui-webapp/            ← Next.js frontend (✅ Complete)
│   ├── app/              ← Main page with UI
│   ├── components/       ← React components
│   └── components/ui/    ← shadcn/ui components
│
├── data/
│   ├── samples/          ← Example images
│   └── cases.csv         ← Test cases (image, question, type)
│
├── docs/
│   └── eval.md
│
├── requirements.txt      ← Python dependencies
├── main.py               ← Entry point for backend
├── run-dev.sh            ← Development runner script
└── README.md             ← This file
```

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dalexaaa/Assistive-VQA.git
cd Assistive-VQA
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ui-webapp
npm install
cd ..
```

---

## Usage

### For End Users

1. Start the application:
```bash
./run-dev.sh
```

2. Open `http://localhost:3000` in your browser

3. Upload an image and ask a question!

### For Developers

**Test backend API:**
```bash
python main.py
```

**Test frontend:**
```bash
cd ui-webapp && npm run dev
```

---

## Current Status

### ✅ Complete (Person 2 - Rajini)
- **UI/Frontend:** Modern Next.js web app with shadcn/ui components
- **Backend API:** Flask server with image upload and routing
- **Integration Logic:** Smart routing between OCR and VQA modules
- **Documentation:** Complete guides for all modules

### 🔄 To Be Completed
- **VQA Module (Person 1):** Implement `answer_question()` - See `/vqa/README.md`
- **OCR Module (Person 3):** Implement `extract_text()` - See `/ocr/README.md`

---

## For Team Members

### Person 1 (Abby) - VQA Module
**Task:** Implement `vqa/vqa_model.py` with `answer_question()` function.  
**Guide:** See `/vqa/README.md` for complete instructions.

### Person 3 - OCR Module
**Task:** Implement `ocr/ocr_module.py` with `extract_text()` function.  
**Guide:** See `/ocr/README.md` for complete instructions.

**No integration work needed!** Just implement your functions and the UI will automatically work.

---

## Documentation

- **UI Module:** `/ui/README.md` - Complete UI documentation
- **Quick Start:** `/ui/QUICK_START.md` - Fast setup guide
- **VQA Guide:** `/vqa/README.md` - VQA implementation
- **OCR Guide:** `/ocr/README.md` - OCR implementation
- **Tests:** `/ui/tests/TEST_RESULTS.md` - Test results

---

## Milestone Deadlines

| Phase | Due Date | Status |
|--------|-----------|--------|
| Modules (VQA, OCR, UI) | **Nov 19** | UI ✅ Complete |
| Integration | **Nov 26** | Ready for testing |
| Final Repo + Demo | **Dec 1** | Pending |

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


## Technology Stack

### Frontend
- **Framework:** Next.js 15 with TypeScript
- **Styling:** Tailwind CSS v4
- **UI Components:** shadcn/ui
- **Features:** Drag-and-drop upload, responsive design

### Backend
- **API Framework:** Flask 3.0
- **Image Processing:** Pillow
- **CORS:** flask-cors

### AI/ML (To be integrated)
- **VQA:** BLIP-2, LLaVA, or similar
- **OCR:** Tesseract + OpenCV

---

## Troubleshooting

### Backend won't start
```bash
pip install -r requirements.txt
python main.py
```

### Frontend won't start
```bash
cd ui-webapp
npm install
npm run dev
```

### "Cannot connect to API"
- Ensure backend is running on port 5000
- Test with: `curl http://localhost:5000/api/health`

---

**Course:** SEA710 - Advanced Computer Vision | **Institution:** Seneca Polytechnic
