#!/bin/bash

echo "Starting System Guardian..."

echo "Starting FastAPI backend on port 8000..."
python app/main.py &
FASTAPI_PID=$!

sleep 3

echo "Starting Flask frontend on port 5000..."
python ui/app.py &
FLASK_PID=$!

echo "System Guardian is running!"
echo "FastAPI: http://localhost:8000"
echo "Flask UI: http://localhost:5000"

wait $FLASK_PID
