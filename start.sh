#!/bin/bash

echo "Starting Chess Web Application..."

# Start backend server
echo "Starting Flask backend server..."
cd backend
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "Starting React frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "Both servers are starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait

# Cleanup
kill $BACKEND_PID
kill $FRONTEND_PID
echo "Servers stopped." 