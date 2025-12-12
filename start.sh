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
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Starting Backend Server..."
# Run in background
python main.py &
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
