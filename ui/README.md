# UI + Integration Module

## Overview

This module provides a modern web-based user interface and backend integration for the Assistive VQA system. It enables users to upload images and ask questions, automatically routing to either the VQA or OCR module based on the question type.

### Architecture

```
┌──────────────────┐
│   Next.js UI     │  ← Frontend (ui-webapp/)
│   (shadcn/ui)    │
└────────┬─────────┘
         │ HTTP
         ▼
┌──────────────────┐
│   Flask API      │  ← Backend (ui/app.py)
│   (Routing Logic)│
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│  VQA  │ │  OCR  │  ← VQA and OCR modules
└───────┘ └───────┘
```

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Install Python Dependencies

```bash
# From project root
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd ui-webapp
npm install
```

### 3. Run the Backend API

```bash
# From project root
python main.py
```

The Flask API will start on `http://localhost:5001`

### 4. Run the Frontend (in a separate terminal)

```bash
cd ui-webapp
npm run dev
```

The Next.js app will start on `http://localhost:3000`

---

## Usage

1. **Open the web interface** at `http://localhost:3000`

2. **Upload an image:**
   - Click the upload area or drag and drop an image
   - Supported formats: PNG, JPG, GIF (max 10MB)

3. **Ask a question:**
   - Type your question in the text area
   - Or click an example question to auto-fill
   - Examples:
     - "What's written on this sign?" (uses OCR)
     - "What color is the car?" (uses VQA)
     - "How many people are in the image?" (uses VQA)
     - "Read the text from this document" (uses OCR)

4. **View the answer:**
   - The system automatically determines whether to use OCR or VQA
   - Results are displayed with the module type used

---

## Integration Logic

### Question Routing Algorithm

The `determine_module()` function in `ui/app.py` analyzes the question and routes it appropriately:

**OCR Keywords (text-related questions):**
- read, text, says, written, word, letter
- sign, label, caption, title, heading
- number, digit, price, address, phone

**VQA Keywords (visual questions):**
- what color, how many, where is, who is
- what is, describe, show, look like
- doing, wearing, holding, scene

**Default:** VQA (if no clear match)

---

## API Endpoints

### `POST /api/query`
Process an image and question.

**Request:**
```bash
curl -X POST http://localhost:5001/api/query \
  -F "image=@path/to/image.jpg" \
  -F "question=What color is the car?"
```

**Response:**
```json
{
  "success": true,
  "answer": "The car is blue.",
  "module": "vqa",
  "question": "What color is the car?"
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Assistive VQA API is running"
}
```

### `POST /api/test`
Check if VQA and OCR modules are available.

**Response:**
```json
{
  "vqa_available": true,
  "ocr_available": true,
  "status": "ready"
}
```

---

## Technology Stack

### Frontend
- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **UI Components:** shadcn/ui
- **Key Libraries:** React 19

### Backend
- **Framework:** Flask 3.0
- **Language:** Python 3.x
- **Key Libraries:**
  - flask-cors (CORS support)
  - Pillow (image processing)
  - werkzeug (file handling)

---

## Component Structure

### Frontend Components (`ui-webapp/components/`)

- **`ImageUploader.tsx`** - Handles image upload via click or drag-and-drop
- **`QuestionInput.tsx`** - Text input for questions with example suggestions
- **`AnswerDisplay.tsx`** - Displays answers with success/error styling

### Backend (`ui/app.py`)

**Key Functions:**
- `determine_module(question)` - Routes questions to appropriate module
- `process_with_ocr(image_path, question)` - Calls OCR module
- `process_with_vqa(image_path, question)` - Calls VQA module
- `query_image()` - Main API endpoint handler

---

## Troubleshooting

### "Failed to connect to the API"
- Make sure Flask backend is running on port 5001
- Check for CORS issues in browser console
- Verify `flask-cors` is installed

### "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Next.js build errors
```bash
cd ui-webapp
rm -rf .next node_modules
npm install
npm run dev
```

### Image upload not working
- Check file size (max 10MB)
- Verify file type is image (PNG, JPG, GIF)
- Check browser console for errors

---

## Team Integration

### For VQA Module:
Implement `vqa/vqa_model.py` with function:
```python
def answer_question(image_path: str, question: str) -> str:
    # Your VQA implementation
    return answer
```

### For OCR Module:
Implement `ocr/ocr_module.py` with function:
```python
def extract_text(image_path: str) -> str:
    # Your OCR implementation
    return extracted_text
```

---
