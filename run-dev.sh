#!/bin/bash

# Assistive VQA - Development Runner
# This script helps run the backend and frontend together

echo "================================================"
echo "  Assistive VQA - Development Mode"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python dependencies are installed
echo -e "${BLUE}Checking Python dependencies...${NC}"
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${RED}Flask not found. Installing dependencies...${NC}"
    pip3 install -r requirements.txt
fi

# Check if Node modules are installed
echo -e "${BLUE}Checking Node.js dependencies...${NC}"
if [ ! -d "ui-webapp/node_modules" ]; then
    echo -e "${RED}Node modules not found. Installing...${NC}"
    cd ui-webapp && npm install && cd ..
fi

echo ""
echo -e "${GREEN}Starting Assistive VQA...${NC}"
echo ""
echo "Backend will run on: http://localhost:5000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo ""
    echo -e "${RED}Stopping servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${BLUE}Starting Flask backend...${NC}"
python3 main.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend
echo -e "${BLUE}Starting Next.js frontend...${NC}"
cd ui-webapp && npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait
