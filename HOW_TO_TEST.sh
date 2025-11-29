#!/bin/bash

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  🚀 Assistive VQA - Quick Test Guide"
echo "═══════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}STEP 1: Start Backend (Flask API)${NC}"
echo "───────────────────────────────────────────────────────"
echo "Run in Terminal 1:"
echo -e "${BLUE}  cd /Users/miracozcan/Desktop/Assistive-VQA${NC}"
echo -e "${BLUE}  python3 main.py${NC}"
echo ""
echo "You should see:"
echo "  ✅ Backend API running on: http://localhost:5001"
echo ""
echo "Press Enter when backend is running..."
read

echo ""
echo -e "${YELLOW}STEP 2: Test Backend API${NC}"
echo "───────────────────────────────────────────────────────"
echo "Testing health check endpoint..."

RESPONSE=$(curl -s -m 5 http://localhost:5001/api/health 2>/dev/null)

if [ $? -eq 0 ] && [ ! -z "$RESPONSE" ]; then
    echo -e "${GREEN}✅ Backend is working!${NC}"
    echo "Response: $RESPONSE"
else
    echo "❌ Backend is not responding"
    echo "Make sure you started it in another terminal with: python3 main.py"
    exit 1
fi

echo ""
echo "Testing module availability..."
curl -s -X POST http://localhost:5001/api/test 2>/dev/null | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))" 2>/dev/null || echo "Modules: VQA and OCR are placeholders (ready for implementation)"

echo ""
echo -e "${YELLOW}STEP 3: Start Frontend (Next.js)${NC}"
echo "───────────────────────────────────────────────────────"
echo "Run in Terminal 2:"
echo -e "${BLUE}  cd /Users/miracozcan/Desktop/Assistive-VQA/ui-webapp${NC}"
echo -e "${BLUE}  npm run dev${NC}"
echo ""
echo "You should see:"
echo "  ✅ Ready in [time]"
echo "  ○ Local: http://localhost:3000"
echo ""
echo "Press Enter when frontend is running..."
read

echo ""
echo -e "${YELLOW}STEP 4: Test in Browser${NC}"
echo "───────────────────────────────────────────────────────"
echo "1. Open: ${BLUE}http://localhost:3000${NC}"
echo "2. You'll see the Assistive VQA interface"
echo "3. Upload any image (drag & drop or click)"
echo "4. Try these questions:"
echo "   • ${GREEN}\"What does the sign say?\"${NC} → Routes to OCR"
echo "   • ${GREEN}\"What color is the car?\"${NC} → Routes to VQA"
echo "   • ${GREEN}\"How many people are there?\"${NC} → Routes to VQA"
echo "5. Click 'Ask Question'"
echo "6. See the answer (currently placeholder text)"
echo ""

echo -e "${YELLOW}STEP 5: Verify Routing${NC}"
echo "───────────────────────────────────────────────────────"
echo "Watch the answer display - it will show:"
echo "  • ${BLUE}\"Processed using OCR module\"${NC} for text questions"
echo "  • ${BLUE}\"Processed using VQA module\"${NC} for visual questions"
echo ""

echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}✅ Testing Guide Complete!${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📝 What's Working:"
echo "   ✅ Backend API (Flask)"
echo "   ✅ Frontend UI (Next.js + shadcn/ui)"
echo "   ✅ Image upload"
echo "   ✅ Question routing logic"
echo "   ✅ API communication"
echo ""
echo "🔄 What Needs Implementation:"
echo "   ⏳ VQA Module (Person 1 - Abby)"
echo "   ⏳ OCR Module (Person 3)"
echo ""
echo "🛑 To Stop:"
echo "   Backend: Press Ctrl+C in Terminal 1"
echo "   Frontend: Press Ctrl+C in Terminal 2"
echo ""
