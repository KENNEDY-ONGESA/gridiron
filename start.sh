#!/bin/bash

# Function to kill processes on exit
cleanup() {
  echo "Stopping servers..."
  kill $(jobs -p) 2>/dev/null
  exit
}

trap cleanup SIGINT SIGTERM

echo "Setting up Backend..."
cd backend

# Detect Python command
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

$PYTHON_CMD -m venv venv

# Activate venv (handle Windows/Linux paths)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt

echo "Starting Backend Server..."
# Run in background
$PYTHON_CMD main.py &
BACKEND_PID=$!

cd ../frontend
echo "Setting up Frontend..."
if [ ! -d "node_modules" ]; then
  npm install
fi

echo "Starting Frontend Server..."
npm run dev &
FRONTEND_PID=$!

echo "Application is running!"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop."

wait
