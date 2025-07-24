#!/bin/bash

# Diagnostic script to help troubleshoot API configuration issues

echo "🔍 Mathopedia API Configuration Diagnostics"
echo "============================================="
echo ""

# Check current location
echo "📍 Current Working Directory:"
echo "   $(pwd)"
echo ""

# Check if .env file exists
echo "📄 Environment File Status:"
if [ -f .env ]; then
    echo "   ✅ .env file exists"
    echo "   📝 Contents:"
    cat .env | while read line; do
        echo "      $line"
    done
else
    echo "   ❌ .env file not found"
    echo "   💡 This means the app will use auto-detection"
fi
echo ""

# Check if we're in the right directory
echo "📂 Directory Check:"
if [ -f package.json ]; then
    echo "   ✅ package.json found - you're in the frontend directory"
    if grep -q "mathopedia-frontend" package.json; then
        echo "   ✅ This is the Mathopedia frontend"
    else
        echo "   ⚠️  This might not be the Mathopedia frontend"
    fi
else
    echo "   ❌ package.json not found"
    echo "   💡 Make sure you're in the frontend directory"
    echo "   📁 Try: cd frontend"
fi
echo ""

# Check if API configuration file exists
echo "🔧 API Configuration:"
if [ -f src/services/api.js ]; then
    echo "   ✅ API service file found"
    
    # Check for auto-detection logic
    if grep -q "window.location.hostname" src/services/api.js; then
        echo "   ✅ Auto-detection logic present"
    else
        echo "   ⚠️  Auto-detection logic might be missing"
    fi
else
    echo "   ❌ API service file not found at src/services/api.js"
fi
echo ""

# Get current network info if possible
echo "🌐 Network Information:"
if command -v hostname >/dev/null 2>&1; then
    echo "   🖥️  Hostname: $(hostname)"
fi

if command -v ifconfig >/dev/null 2>&1; then
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
    if [ ! -z "$LOCAL_IP" ]; then
        echo "   📡 Local IP: $LOCAL_IP"
        echo "   💡 If accessing from other devices, your backend should be at: http://$LOCAL_IP:5000"
    fi
elif command -v ip >/dev/null 2>&1; then
    LOCAL_IP=$(ip route get 1 | sed 's/^.*src \([^ ]*\).*$/\1/;q')
    if [ ! -z "$LOCAL_IP" ]; then
        echo "   📡 Local IP: $LOCAL_IP"
        echo "   💡 If accessing from other devices, your backend should be at: http://$LOCAL_IP:5000"
    fi
fi
echo ""

# Recommendations
echo "🎯 Recommendations:"
echo ""

if [ ! -f .env ]; then
    echo "   📝 No .env file found. The app will use auto-detection:"
    echo "      - Development: Auto-detects your current host"
    echo "      - Production: Uses relative URLs"
    echo "      - This should work for most deployments"
    echo ""
    echo "   🚀 If you want explicit control, run:"
    echo "      ./setup-env.sh"
else
    echo "   📝 .env file found. The app will use your configured settings."
    echo ""
    if grep -q "REACT_APP_API_URL=.*localhost" .env; then
        echo "   ⚠️  You have localhost configured - this might cause issues when"
        echo "      accessing from other devices/networks."
        echo ""
        echo "   🔧 To fix this, either:"
        echo "      1. Remove the .env file to use auto-detection"
        echo "      2. Run ./setup-env.sh to reconfigure"
        echo "      3. Manually edit .env with your server's IP"
    fi
fi

echo ""
echo "🔧 Quick Fixes:"
echo ""
echo "   Problem: API calls go to localhost when accessing from different IP"
echo "   Solution 1 (Auto-detection):"
echo "      rm .env"
echo "      npm start"
echo ""
echo "   Solution 2 (Manual configuration):"
echo "      echo 'REACT_APP_API_URL=http://YOUR_SERVER_IP:5000' > .env"
echo "      npm start"
echo ""
echo "   Solution 3 (Interactive setup):"
echo "      ./setup-env.sh"
echo ""

echo "============================================="
echo "🎉 Diagnostics Complete!"
