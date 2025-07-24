#!/bin/bash

# Development Start Script
# This script starts all components of the Mathopedia application

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

echo "🚀 Starting Mathopedia Development Environment..."

# Check if MySQL is running (optional - can be PostgreSQL too)
if ! pgrep -x "mysqld" > /dev/null && ! pgrep -x "postgres" > /dev/null; then
    echo "⚠️  Neither MySQL nor PostgreSQL is detected running."
    echo "   Please ensure your database is running first."
    echo "   - For MySQL: brew services start mysql"
    echo "   - For PostgreSQL: brew services start postgresql"
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    if pgrep -x "mysqld" > /dev/null; then
        echo "✅ MySQL is running"
    fi
    if pgrep -x "postgres" > /dev/null; then
        echo "✅ PostgreSQL is running"
    fi
fi

# Check if backend port is available
if check_port 5000; then
    echo "⚠️  Port 5000 is already in use. Backend might already be running."
else
    echo "🐍 Starting Python backend..."
    cd backend
    
    # Check if virtual environment exists, create if not
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        echo "📥 Installing dependencies..."
        pip install -r requirements.txt
    else
        source venv/bin/activate
    fi
    
    echo "🚀 Starting backend server..."
    python run.py &
    BACKEND_PID=$!
    echo "✅ Backend started (PID: $BACKEND_PID)"
    cd ..
fi

# Wait a moment for backend to start
sleep 3

# Check if frontend port is available
if check_port 3000; then
    echo "⚠️  Port 3000 is already in use. Frontend might already be running."
else
    echo "⚛️  Starting React frontend..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
    cd ..
fi

echo ""
echo "🎉 Mathopedia is starting up!"
echo ""
echo "🌐 URLs:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:5000"
echo ""
echo "📊 To check status:"
echo "- Frontend: curl http://localhost:3000"
echo "- Backend: curl http://localhost:5000"
echo ""
echo "🛑 To stop the application:"
echo "- Press Ctrl+C in the terminals"
echo "- Or run: pkill -f 'python run.py' && pkill -f 'npm start'"
echo ""
echo "📝 Logs:"
echo "- Check the terminal windows for backend and frontend logs"
echo "- Backend logs will show API requests and database operations"
echo "- Frontend logs will show React compilation and errors"

# Keep script running
wait
