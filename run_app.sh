#!/usr/bin/env bash
# Automated startup script for Citizen Grievance Application

echo "============================================================"
echo " Starting Citizen Grievance Application (100% Full System) "
echo "============================================================"

# Start backend FastAPI server in background
cd backend
source venv/bin/activate
python app/main.py &
BACKEND_PID=$!
echo "FastAPI Backend started on http://localhost:8000 (PID: $BACKEND_PID)"

# Start frontend Vite server
cd ../frontend
npm run dev &
FRONTEND_PID=$!
echo "Vite Frontend started on http://localhost:5173 (PID: $FRONTEND_PID)"

echo "============================================================"
echo " Application is running cleanly!"
echo " Backend API: http://localhost:8000"
echo " Frontend Web: http://localhost:5173"
echo " Press Ctrl+C to stop both processes."
echo "============================================================"

wait
