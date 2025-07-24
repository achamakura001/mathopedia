#!/bin/bash

# Mathopedia Development Setup Script
# This script sets up the entire Mathopedia application for development

set -e  # Exit on any error

echo "🔧 Setting up Mathopedia Development Environment..."

# Check if required tools are installed
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v mysql >/dev/null 2>&1 || { echo "❌ MySQL is required but not installed. Aborting." >&2; exit 1; }

echo "✅ All required tools found!"

# Setup Backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Created Python virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
echo "✅ Installed Python dependencies"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file - please update with your database credentials"
    echo "⚠️  IMPORTANT: Update the .env file with your MySQL credentials before continuing!"
    read -p "Press Enter after updating the .env file..."
fi

# Initialize database
echo "🗄️  Initializing database..."
python run.py init-db
python run.py seed-db
echo "✅ Database initialized and seeded"

cd ..

# Setup Frontend
echo "⚛️  Setting up React frontend..."
cd frontend

# Install dependencies
npm install
echo "✅ Installed Node.js dependencies"

cd ..

# Setup Question Generator
echo "🤖 Setting up Question Generator..."
cd question-generator

# Install dependencies
pip install -r requirements.txt
echo "✅ Installed Question Generator dependencies"

cd ..

echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure MySQL is running"
echo "2. Make sure Ollama is running (if using local LLM): ollama serve"
echo "3. Start the backend: cd backend && source venv/bin/activate && python run.py"
echo "4. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 URLs:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:5000"
echo ""
echo "🚀 Happy coding!"
