#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting BOM to Order Application${NC}\n"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama is not installed. Please install from https://ollama.ai${NC}"
    exit 1
fi

# Check if the model is available
if ! ollama list | grep -q "llama3.2:1b"; then
    echo -e "${BLUE}📥 Pulling llama3.2:1b model...${NC}"
    ollama pull llama3.2:1b
fi

# Check if API key exists
if [ ! -f "API_Key.txt" ]; then
    echo -e "${RED}⚠️  Warning: API_Key.txt not found. Gemini API features may not work.${NC}"
    echo -e "${RED}   Create API_Key.txt with your Google Gemini API key${NC}\n"
fi

# Check if Python dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    pip install -r backend/requirements.txt
fi

# Start backend server in background
echo -e "${GREEN}🐍 Starting Backend Server (Flask)...${NC}"
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:5000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend running on http://localhost:5000${NC}\n"
else
    echo -e "${RED}❌ Failed to start backend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend server
echo -e "${GREEN}⚛️  Starting Frontend Server (Vite)...${NC}"
cd "BOM to Order/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    pnpm install
fi

pnpm dev &
FRONTEND_PID=$!
cd ../..

echo -e "\n${GREEN}✅ Both servers are running!${NC}"
echo -e "${BLUE}Frontend: http://localhost:5173${NC}"
echo -e "${BLUE}Backend:  http://localhost:5000${NC}"
echo -e "\n${GREEN}Press Ctrl+C to stop all servers${NC}\n"

# Trap Ctrl+C to kill both processes
trap "echo -e '\n${RED}🛑 Stopping servers...${NC}'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Wait for processes
wait
