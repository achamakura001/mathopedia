#!/bin/bash

# Setup script for creating .env file based on deployment type

echo "=== Mathopedia Frontend Environment Setup ==="
echo ""
echo "This script will help you create a .env file for your deployment."
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "Warning: .env file already exists."
    read -p "Do you want to overwrite it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

echo "Please select your deployment type:"
echo "1) Development (backend on localhost:5000)"
echo "2) Production with custom backend URL"
echo "3) Same-host deployment (relative URLs)"
echo "4) Docker/containerized deployment"
echo "5) Auto-detect (recommended for most cases)"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "REACT_APP_API_URL=http://localhost:5000" > .env
        echo "✅ Created .env for development setup"
        ;;
    2)
        read -p "Enter your backend URL (e.g., http://your-server:5000): " backend_url
        echo "REACT_APP_API_URL=$backend_url" > .env
        echo "✅ Created .env for production setup with custom URL"
        ;;
    3)
        echo "# Using relative URLs for same-host deployment" > .env
        echo "# REACT_APP_API_URL=" >> .env
        echo "✅ Created .env for same-host deployment"
        ;;
    4)
        read -p "Enter your backend service name (e.g., backend): " service_name
        echo "REACT_APP_API_URL=http://$service_name:5000" > .env
        echo "✅ Created .env for Docker deployment"
        ;;
    5)
        echo "# Auto-detect configuration - no explicit API URL needed" > .env
        echo "# The app will automatically detect your host and configure API calls" >> .env
        echo "✅ Created .env for auto-detection mode"
        echo "📝 The app will automatically use the same host as your frontend with port 5000"
        ;;
    *)
        echo "❌ Invalid choice. Setup cancelled."
        exit 1
        ;;
esac

echo ""
echo "✅ Environment configuration complete!"
echo "Your .env file has been created. You can edit it manually if needed."
echo ""
echo "To start the application:"
echo "  npm start"
