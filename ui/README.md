# UI + Integration Module

**Owner:** Person 2 (Rajini)  
**Responsibilities:** User interface + integration logic between VQA and OCR modules

---

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
│  VQA  │ │  OCR  │  ← Modules by Person 1 & 3
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
# Navigate to frontend directory
cd ui-webapp

# Install dependencies
npm install
```

### 3. Run the Backend API

```bash
# From project root
python main.py
```

The Flask API will start on `http://localhost:5000`

### 4. Run the Frontend (in a separate terminal)

```bash
# From ui-webapp directory
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

### API Endpoints

#### `POST /api/query`
Process an image and question.

**Request:**
```bash
curl -X POST http://localhost:5000/api/query \
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

#### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Assistive VQA API is running"
}
```

#### `POST /api/test`
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
- **Key Libraries:**
  - React 19
  - Next.js Image optimization

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

#### `ImageUploader.tsx`
- Handles image upload via click or drag-and-drop
- Validates file type and size
- Displays image preview
- Uses Next.js Image component for optimization

#### `QuestionInput.tsx`
- Text input for questions
- Example question suggestions
- Enter key support for quick submission
- Loading state handling

#### `AnswerDisplay.tsx`
- Displays answers with success styling
- Shows error messages
- Loading spinner during processing
- "Start Over" functionality

### Backend (`ui/app.py`)

#### Key Functions:
- `determine_module(question)` - Routes questions to appropriate module
- `process_with_ocr(image_path, question)` - Calls OCR module
- `process_with_vqa(image_path, question)` - Calls VQA module
- `query_image()` - Main API endpoint handler

---

## Test Examples

### Test Case 1: Text Recognition
**Image:** Street sign with "STOP"  
**Question:** "What does the sign say?"  
**Expected Module:** OCR  
**Expected Answer:** "STOP"

### Test Case 2: Object Identification
**Image:** Photo of a red car  
**Question:** "What color is the car?"  
**Expected Module:** VQA  
**Expected Answer:** "The car is red"

### Test Case 3: Counting
**Image:** Group photo with 5 people  
**Question:** "How many people are in this image?"  
**Expected Module:** VQA  
**Expected Answer:** "There are 5 people"

### Test Case 4: Document Reading
**Image:** Business card  
**Question:** "What is the phone number?"  
**Expected Module:** OCR  
**Expected Answer:** (extracted phone number)

### Test Case 5: Scene Description
**Image:** Park scene  
**Question:** "Describe what you see"  
**Expected Module:** VQA  
**Expected Answer:** (description of the park scene)

---

## Development Notes

### Running in Development Mode

**Backend:**
```bash
# From project root
python main.py
# or
cd ui && python app.py
```

**Frontend:**
```bash
cd ui-webapp
npm run dev
```

### Building for Production

**Frontend:**
```bash
cd ui-webapp
npm run build
npm start
```

**Backend:**
Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 ui.app:app
```

### Environment Variables

Create a `.env.local` file in `ui-webapp/`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## Accessibility Features

- High contrast UI elements
- Keyboard navigation support
- Screen reader friendly labels
- Clear error messages
- Large touch targets for mobile
- Responsive design for all screen sizes

---

## Future Enhancements

- [ ] Camera capture support for mobile devices
- [ ] Voice input for questions (speech-to-text)
- [ ] Voice output for answers (text-to-speech)
- [ ] History of previous queries
- [ ] Multi-language support
- [ ] Batch processing of multiple images
- [ ] Export results to PDF/text file

---

## Troubleshooting

### "Failed to connect to the API"
- Make sure Flask backend is running on port 5000
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

### For VQA Module Owner (Person 1):
- Implement `vqa/vqa_model.py` with function:
  ```python
  def answer_question(image_path: str, question: str) -> str:
      # Your VQA implementation
      return answer
  ```

### For OCR Module Owner (Person 3):
- Implement `ocr/ocr_module.py` with function:
  ```python
  def extract_text(image_path: str) -> str:
      # Your OCR implementation
      return extracted_text
  ```

The integration will automatically work once these functions are implemented!

---

## Contact

**Module Owner:** Person 2 (Rajini)  
**Last Updated:** November 24, 2025
