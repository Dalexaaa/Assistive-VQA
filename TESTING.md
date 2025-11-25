# 🧪 How to Test the System

## Quick Test (2 Steps)

### Terminal 1: Start Backend
```bash
cd /Users/miracozcan/Desktop/Assistive-VQA
python3 main.py
```

**Expected output:**
```
============================================================
Assistive VQA System
============================================================

Backend API running on: http://localhost:5001
...
```

✅ Leave this terminal running

---

### Terminal 2: Start Frontend
```bash
cd /Users/miracozcan/Desktop/Assistive-VQA/ui-webapp
npm run dev
```

**Expected output:**
```
▲ Next.js 15.x.x
- Local:        http://localhost:3000
✓ Ready in [time]
```

✅ Leave this terminal running

---

### Browser: Test the UI

1. **Open:** http://localhost:3000

2. **Upload an image:**
   - Click the upload area, OR
   - Drag and drop any image

3. **Ask a question:**
   - Type: "What does the sign say?" (tests OCR routing)
   - Or click an example question

4. **Click "Ask Question"**

5. **See the result:**
   - Shows which module was used (OCR or VQA)
   - Displays placeholder answer (real answers come after VQA/OCR are implemented)

---

## Test Different Question Types

### OCR Questions (text extraction):
- ✅ "What does the sign say?"
- ✅ "Read the text from this image"
- ✅ "What is written on the label?"
- ✅ "What is the phone number?"

### VQA Questions (visual analysis):
- ✅ "What color is the car?"
- ✅ "How many people are in this image?"
- ✅ "Describe what you see"
- ✅ "What is this person doing?"

The answer will show: **"Processed using [OCR/VQA] module"**

---

## Manual API Testing (Optional)

If you want to test the backend directly without the UI:

### Test 1: Health Check
```bash
curl http://localhost:5001/api/health
```

**Expected:**
```json
{"status":"ok","message":"Assistive VQA API is running"}
```

### Test 2: Module Availability
```bash
curl -X POST http://localhost:5001/api/test
```

**Expected:**
```json
{
  "vqa_available": true,
  "ocr_available": true,
  "status": "partial"
}
```
*(Both show true because placeholder modules exist)*

### Test 3: Query with Image
```bash
# Create a test
curl -X POST http://localhost:5001/api/query \
  -F "image=@/path/to/your/image.jpg" \
  -F "question=What color is the car?"
```

**Expected:**
```json
{
  "success": true,
  "answer": "VQA Module: I can see the image... (placeholder)",
  "module": "vqa",
  "question": "What color is the car?"
}
```

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 5001 is in use
lsof -i:5001

# Kill process if needed
lsof -ti:5001 | xargs kill -9

# Restart
python3 main.py
```

### Frontend won't start
```bash
cd ui-webapp
rm -rf .next node_modules
npm install
npm run dev
```

### "Cannot connect to API" in browser
1. Make sure backend is running on port 5001
2. Check browser console for errors (F12)
3. Verify: `curl http://localhost:5001/api/health`

### Port 5001 already in use
The app will automatically try to use a different port. Check the terminal output for the actual port.

---

## What You Should See

### Backend Terminal:
```
* Running on http://127.0.0.1:5001
* Debugger is active!
```

### Frontend Terminal:
```
✓ Ready in 1.2s
○ Local:   http://localhost:3000
```

### Browser at http://localhost:3000:
- Beautiful gradient UI with "Assistive VQA" header
- Image upload area
- Question input with example questions
- Answer display area

---

## Current Status

✅ **Working:**
- Frontend UI (beautiful, responsive)
- Backend API (Flask)
- Image upload
- Question routing
- API communication
- Error handling

⏳ **Placeholder (needs implementation by teammates):**
- VQA Module (Person 1 - will replace placeholder)
- OCR Module (Person 3 - will replace placeholder)

---

## For Your Teammates

Once you implement your modules:
1. The system will automatically use your real implementation
2. No changes to integration code needed
3. Just keep the same function signatures:
   - `vqa/vqa_model.py`: `answer_question(image_path, question)`
   - `ocr/ocr_module.py`: `extract_text(image_path)`

---

## Stop the System

**Backend:** Press `Ctrl+C` in Terminal 1  
**Frontend:** Press `Ctrl+C` in Terminal 2

---

Need help? Check:
- `/ui/README.md` - Complete documentation
- `/ui/QUICK_START.md` - Quick setup guide
- `/vqa/README.md` - VQA implementation guide
- `/ocr/README.md` - OCR implementation guide
