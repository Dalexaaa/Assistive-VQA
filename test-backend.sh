#!/bin/bash

echo "🧪 Testing Assistive VQA System"
echo "================================"
echo ""

# Check if backend is running
echo "1️⃣  Checking backend..."
if lsof -ti:5001 > /dev/null 2>&1; then
    echo "   ✅ Backend is running on port 5001"
else
    echo "   ❌ Backend is NOT running"
    echo "   Starting backend..."
    cd "$(dirname "$0")"
    python3 main.py > backend.log 2>&1 &
    BACKEND_PID=$!
    echo "   Backend started (PID: $BACKEND_PID)"
    sleep 3
fi

echo ""
echo "2️⃣  Testing API Health Check..."
HEALTH=$(curl -s http://localhost:5001/api/health 2>/dev/null)
if [ ! -z "$HEALTH" ]; then
    echo "   ✅ API is responding"
    echo "   Response: $HEALTH"
else
    echo "   ❌ API is not responding"
    echo "   Check backend.log for errors"
    exit 1
fi

echo ""
echo "3️⃣  Testing Module Availability..."
MODULES=$(curl -s -X POST http://localhost:5001/api/test 2>/dev/null)
echo "   $MODULES"

echo ""
echo "================================"
echo "✅ Backend Testing Complete!"
echo ""
echo "📝 Next Steps:"
echo "   1. Open a NEW terminal"
echo "   2. Run: cd ui-webapp && npm run dev"
echo "   3. Open browser: http://localhost:3000"
echo ""
echo "🔍 Manual API Testing:"
echo "   Health Check: curl http://localhost:5001/api/health"
echo "   Module Test:  curl -X POST http://localhost:5001/api/test"
echo ""
echo "🛑 To stop backend: kill \$(lsof -ti:5001)"
echo "================================"
