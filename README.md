# Assistive-VQA (SEA710 Project)
This project aims to create an assistive system that can answer visual questions about images,
helping visually impaired users understand their surroundings.

---

## Team Members

| Role | Member | Description |
|------|---------|-------------|
| Person 1 | Abby | VQA + Repository Setup |
| Person 2 | Mirac | UI + Integration of VQA and OCR |
| Person 3 | Rajini | OCR + Final Report |

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

## System Requirements

- **Python:** 3.8 or higher
- **Node.js:** 18.0 or higher (for Next.js frontend)
- **Tesseract OCR:** Must be installed separately on your system
  - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Dalexaaa/Assistive-VQA.git
cd Assistive-VQA
```

### 2. Set Up Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install PyTorch (REQUIRED - Install First!)

PyTorch must be installed **before** other dependencies. Choose the appropriate command for your system:

**CPU-only (No GPU):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**NVIDIA GPU with CUDA 12.1 (Windows/Linux):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Apple Silicon M1/M2/M3 (macOS):**
```bash
pip install torch torchvision torchaudio
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Frontend Dependencies
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

## Documentation

- **UI Module:** `/ui/README.md` - Complete UI documentation
- **Quick Start:** `/ui/QUICK_START.md` - Fast setup guide
- **VQA Guide:** `/vqa/README.md` - VQA implementation
- **OCR Guide:** `/ocr/README.md` - OCR implementation
- **Tests:** `/ui/tests/TEST_RESULTS.md` - Test results

---

## Testing

Each module includes comprehensive testing:

- **VQA Module:** Test cases in `/vqa/test_vqa.py`
- **OCR Module:** Test cases in `/ocr/ocr-app/`
- **UI/Integration:** Test cases in `/ui/tests/`
- **Sample Data:** Test images in `/data/samples/`

Run tests individually:
```bash
python vqa/test_vqa.py
python ocr/ocr_module.py
```

---

## System Architecture

The system uses a smart routing mechanism to determine whether to use OCR or VQA:

1. **User Input:** Image + Question via Next.js frontend
2. **Flask Backend (`ui/app.py`):** Receives request and analyzes question
3. **Smart Routing:** Determines module based on question keywords:
   - Text-related questions ("read", "text", "says") → **OCR Module**
   - Visual questions ("what", "describe", "color") → **VQA Module**
4. **Response:** Answer returned to frontend and displayed to user

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

### AI/ML
- **VQA:** BLIP-2 (Salesforce) - Visual Question Answering
- **OCR:** Tesseract + OpenCV - Text extraction with preprocessing


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
