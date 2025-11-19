#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping servers..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID
    fi
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# Start Backend
echo "Starting Backend..."
# Ensure we are in the root directory
cd "$(dirname "$0")"
backend/myenv/bin/python3 backend/app.py &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# Start Frontend
echo "Starting Frontend..."
cd frontend
REACT_APP_API_URL=http://127.0.0.1:5000 npm start
