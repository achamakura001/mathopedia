#!/bin/bash

# Mathopedia System Setup Script
# This script sets up the complete Mathopedia system on a new machine

set -e  # Exit on any error

echo "🚀 Setting up Mathopedia on new system..."

# Check if we're in the right directory
if [ ! -f "package.json" ] && [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Please run this script from the Mathopedia project root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install MySQL on different systems
install_mysql() {
    echo "📦 Installing MySQL..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command_exists brew; then
            brew install mysql
            brew services start mysql
        else
            echo "❌ Homebrew not found. Please install MySQL manually."
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command_exists apt-get; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y mysql-server mysql-client
            sudo systemctl start mysql
            sudo systemctl enable mysql
        elif command_exists yum; then
            # CentOS/RHEL
            sudo yum install -y mysql-server mysql
            sudo systemctl start mysqld
            sudo systemctl enable mysqld
        else
            echo "❌ Unsupported Linux distribution. Please install MySQL manually."
            exit 1
        fi
    else
        echo "❌ Unsupported operating system. Please install MySQL manually."
        exit 1
    fi
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check Node.js
if ! command_exists node; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check npm
if ! command_exists npm; then
    echo "❌ npm is required but not installed."
    exit 1
fi

# Check MySQL
if ! command_exists mysql; then
    echo "⚠️  MySQL not found. Would you like to install it? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        install_mysql
    else
        echo "❌ MySQL is required. Please install it manually."
        exit 1
    fi
fi

echo "✅ All prerequisites found!"

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo "⚙️  Setting up environment variables..."
if [ ! -f .env ]; then
    cat > .env << EOF
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root123
MYSQL_DB=mathopedia

# Security
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# LLM Configuration (Optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here
EOF
    echo "📝 Created .env file with default configuration"
    echo "⚠️  Please update the database password in backend/.env if needed"
else
    echo "📝 .env file already exists"
fi

# Setup database
echo "🗄️  Setting up database..."
# Create database
mysql -u root -e "CREATE DATABASE IF NOT EXISTS mathopedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null || {
    echo "⚠️  Could not create database automatically. Please create it manually:"
    echo "   mysql -u root -p"
    echo "   CREATE DATABASE mathopedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
}

# Run migrations
echo "🔄 Running database migrations..."
python -m flask db upgrade 2>/dev/null || {
    echo "🏗️  Initializing database migrations..."
    python -m flask db init
    python -m flask db migrate -m "Initial migration"
    python -m flask db upgrade
}

# Seed data
echo "🌱 Seeding database with sample data..."
python -c "
from app.services.topic_seeder import seed_topics
from app.services.question_seeder import seed_questions
seed_topics()
seed_questions()
print('✅ Database seeded successfully!')
"

cd ..

# Setup frontend
echo "⚛️  Setting up frontend..."
cd frontend
npm install

cd ..

echo "✅ System setup completed successfully!"
echo ""
echo "🎉 Mathopedia is ready to run!"
echo ""
echo "To start the application:"
echo "1. Start the backend:"
echo "   cd backend && source .venv/bin/activate && python run.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend && npm start"
echo ""
echo "3. Access the application at http://localhost:3000"
echo ""
echo "📚 API documentation available at http://localhost:5000/api/v2/docs/"
