@echo off
SETLOCAL

:: Function to handle cleanup on exit is harder in Batch, relying on user to close windows.

echo Setting up Backend...
cd backend
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt

echo Starting Backend Server...
:: Start in a new window so we can see logs
start "Backend Server" python main.py

cd ..\frontend
echo Setting up Frontend...
if not exist node_modules (
  call npm install
)

echo Starting Frontend Server...
:: Start in a new window
start "Frontend Server" npm run dev

echo Application is running!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo Close the new windows to stop the servers.
pause
