# Quick Fix: API Configuration Issue

## Problem
API calls go to localhost instead of your server's hostname/IP when accessing from different devices.

## ✅ NEW: Auto-Detection Solution
The app now automatically detects your host! **No configuration needed in most cases.**

1. **Remove any existing .env file** (if you have one with localhost):
   ```bash
   cd frontend
   rm .env  # Remove old configuration
   npm start
   ```

2. **The app will automatically**:
   - Detect your current IP/hostname
   - Route API calls to the same host on port 5000
   - Work when accessed from any device on your network

## Manual Configuration (if needed)

1. **Quick Setup (Recommended):**
   ```bash
   cd frontend
   ./setup-env.sh
   ```

2. **Manual Setup:**
   ```bash
   cd frontend
   echo "REACT_APP_API_URL=http://YOUR_SERVER_IP:5000" > .env
   npm start
   ```

3. **Diagnostic Tool:**
   ```bash
   cd frontend
   ./diagnose.sh  # Check your current configuration
   ```

## Examples

| Your Setup | Configuration |
|------------|--------------|
| Auto-detection (recommended) | No .env file needed |
| Development | `REACT_APP_API_URL=http://localhost:5000` |
| Different Server | `REACT_APP_API_URL=http://192.168.1.100:5000` |
| Same Host | `REACT_APP_API_URL=` (empty) |
| Docker | `REACT_APP_API_URL=http://backend:5000` |

## How Auto-Detection Works

- **Development**: If you access via IP (like `http://192.168.1.100:3000`), API calls go to `http://192.168.1.100:5000`
- **Development**: If you access via localhost, API calls go to `http://localhost:5000`
- **Production**: Uses relative URLs (works with reverse proxies)

## Important Notes
- Must restart app after changing .env file
- Auto-detection works without any configuration
- Check browser console for API configuration debug info

## Still Having Issues?
Run the diagnostic tool: `./diagnose.sh`
See the full [Deployment Guide](../DEPLOYMENT_GUIDE.md) for detailed troubleshooting.
