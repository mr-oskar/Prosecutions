#!/bin/bash

echo "========================================="
echo "  System Guardian - Starting Services"
echo "========================================="
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.11 or higher."
    exit 1
fi

echo "Python found: $(python3 --version)"
echo ""

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/Updating dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "Creating required directories..."
mkdir -p db reports/pdfs reports/json

echo ""
echo "========================================="
echo "  Starting FastAPI Backend Server"
echo "========================================="
echo "Backend will run on: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 3

echo ""
echo "========================================="
echo "  Starting Flask Web Interface"
echo "========================================="
echo "Web Interface will run on: http://localhost:5000"
echo "Admin Panel: http://localhost:5000/admin"
echo ""

python ui/app.py &
FRONTEND_PID=$!

echo ""
echo "========================================="
echo "  Both servers are running!"
echo "========================================="
echo ""
echo "  Web Interface: http://localhost:5000"
echo "  Admin Panel:   http://localhost:5000/admin"
echo "  API Docs:      http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================="

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
