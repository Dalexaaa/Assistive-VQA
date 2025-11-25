# Quick Start Guide - UI Module

## For Testing the UI (Right Now!)

### 1. Install Backend Dependencies

```bash
# From project root
pip install flask flask-cors pillow
```

### 2. Start the Backend

```bash
python main.py
```

You should see:
```
============================================================
Assistive VQA System
============================================================

Backend API running on: http://localhost:5000
Frontend (Next.js): Run 'npm run dev' in ui-webapp/ directory
...
```

### 3. Start the Frontend (New Terminal)

```bash
cd ui-webapp
npm run dev
```

### 4. Open Your Browser

Navigate to: `http://localhost:3000`

### 5. Test the Interface

1. **Upload an image** (any image from your computer)
2. **Type a question** or click an example:
   - "What's written on this sign?"
   - "What color is the car?"
   - "How many people are in this image?"
3. **Click "Ask Question"**
4. **See the result** - it will show which module was used (OCR or VQA)

**Note:** Currently using placeholder modules. Real answers will appear once Person 1 and Person 3 implement their modules!

---

## Architecture Overview

```
User Browser (localhost:3000)
         ↓
    Next.js UI (TypeScript + shadcn/ui)
         ↓ HTTP POST
    Flask API (localhost:5000)
         ↓
   Routing Logic (determines OCR vs VQA)
         ↓
    ┌─────────┴─────────┐
    ↓                   ↓
VQA Module          OCR Module
(Person 1)          (Person 3)
```

---

## What's Already Done

✅ **Frontend (Next.js + shadcn/ui)**
- Beautiful, responsive UI
- Image upload (click or drag-drop)
- Question input with examples
- Answer display with loading states
- Error handling

✅ **Backend (Flask API)**
- Image upload handling
- Question routing logic
- Integration with VQA/OCR modules
- CORS support for frontend
- Health check endpoints

✅ **Integration Logic**
- Automatic module detection based on question
- Smart routing between OCR and VQA
- Placeholder modules for testing
- Ready for real module implementation

✅ **Documentation**
- Complete README for UI module
- Test case documentation
- Integration guides for teammates

---

## For Teammates

### Person 1 (Abby - VQA):
Your module will be called automatically when users ask visual questions!

**What you need to do:**
1. Implement `vqa/vqa_model.py`:
```python
def answer_question(image_path: str, question: str) -> str:
    # Your BLIP-2 or LLaVA implementation
    return "Your answer here"
```

2. Add your dependencies to `requirements.txt`
3. Test with: `python vqa/vqa_model.py`

**No integration code needed!** Just implement the function and it works.

---

### Person 3 (OCR):
Your module will be called automatically when users ask about text!

**What you need to do:**
1. Implement `ocr/ocr_module.py`:
```python
def extract_text(image_path: str) -> str:
    # Your Tesseract implementation
    return "Extracted text here"
```

2. Add your dependencies to `requirements.txt`
3. Test with: `python ocr/ocr_module.py`

**No integration code needed!** Just implement the function and it works.

---

## Testing Your Module with the UI

### Once You've Implemented Your Module:

1. **Start the backend:**
```bash
python main.py
```

2. **Start the frontend:**
```bash
cd ui-webapp && npm run dev
```

3. **Test in browser:**
   - Upload test images
   - Ask relevant questions
   - See your module's real responses!

4. **Check which module is being used:**
   - The UI shows "Processed using VQA module" or "OCR module"
   - Verify correct routing

---

## API Testing (Without UI)

You can test the backend directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Test module availability
curl -X POST http://localhost:5000/api/test

# Query with image
curl -X POST http://localhost:5000/api/query \
  -F "image=@path/to/image.jpg" \
  -F "question=What color is the car?"
```

---

## File Structure

```
Assistive-VQA/
├── ui/
│   ├── app.py              # Flask backend API ✅
│   ├── README.md           # This documentation ✅
│   └── tests/
│       └── TEST_RESULTS.md # Test cases ✅
│
├── ui-webapp/              # Next.js frontend ✅
│   ├── app/
│   │   └── page.tsx        # Main page ✅
│   ├── components/
│   │   ├── ImageUploader.tsx   ✅
│   │   ├── QuestionInput.tsx   ✅
│   │   └── AnswerDisplay.tsx   ✅
│   └── components/ui/      # shadcn components ✅
│
├── vqa/
│   ├── vqa_model.py        # Your implementation here (Person 1)
│   └── README.md           # Implementation guide ✅
│
├── ocr/
│   ├── ocr_module.py       # Your implementation here (Person 3)
│   └── README.md           # Implementation guide ✅
│
├── main.py                 # Entry point ✅
└── requirements.txt        # Dependencies ✅
```

---

## Common Issues

### "Module not found: flask"
```bash
pip install flask flask-cors pillow
```

### "Cannot connect to API"
- Make sure Flask is running on port 5000
- Check terminal for errors
- Try: `curl http://localhost:5000/api/health`

### Frontend errors
```bash
cd ui-webapp
rm -rf .next node_modules
npm install
npm run dev
```

---

## Next Steps

1. ✅ UI Module complete (Person 2 - Me)
2. ⏳ VQA Module (Person 1 - Abby)
3. ⏳ OCR Module (Person 3)
4. 📅 Integration Testing (Nov 26)
5. 🎯 Final Demo (Dec 1)

---

## Questions?

Check the full documentation in:
- `/ui/README.md` - Complete UI documentation
- `/vqa/README.md` - VQA implementation guide  
- `/ocr/README.md` - OCR implementation guide
