# API Configuration Guide

This document explains how to configure the frontend to connect to your backend API in different deployment scenarios.

## Configuration Options

The frontend uses the `REACT_APP_API_URL` environment variable to determine where to send API requests.

### 1. Development Setup

For local development with backend running on `localhost:5000`:

```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:5000" > .env
```

### 2. Production with Custom Backend URL

When your backend is hosted on a different server or port:

```bash
# Example: Backend on different server
REACT_APP_API_URL=http://192.168.1.100:5000

# Example: Backend on different domain
REACT_APP_API_URL=https://api.yourdomain.com

# Example: Backend on different port
REACT_APP_API_URL=http://yourserver.com:8080
```

### 3. Same-Host Deployment

When frontend and backend are served from the same host/port (e.g., using a reverse proxy):

```bash
# Leave REACT_APP_API_URL empty or don't set it
# This uses relative URLs like /api/auth/login
```

### 4. Docker/Container Deployment

When using Docker Compose or similar containerized setup:

```bash
# Use the backend service name
REACT_APP_API_URL=http://backend:5000
```

## Automatic Configuration

The app includes smart defaults:

- **Development**: Falls back to `http://localhost:5000` if no URL is set
- **Production**: Uses relative URLs if no URL is set (good for same-host deployments)
- **Explicit**: Always uses the exact URL if `REACT_APP_API_URL` is set

## Setup Methods

### Method 1: Automatic Setup Script

Run the interactive setup script:

```bash
cd frontend
./setup-env.sh
```

### Method 2: Manual Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your API URL:
   ```bash
   REACT_APP_API_URL=http://your-backend-url:port
   ```

### Method 3: Environment Variables

Set the environment variable directly when running:

```bash
REACT_APP_API_URL=http://your-backend:5000 npm start
```

## Troubleshooting

### Issue: API calls go to localhost instead of your server

**Cause**: The `REACT_APP_API_URL` environment variable is not set correctly.

**Solutions**:
1. Create a `.env` file in the frontend directory with the correct API URL
2. Restart the development server after changing environment variables
3. Check that your `.env` file is in the correct location (`frontend/.env`)

### Issue: CORS errors

**Cause**: Backend CORS configuration doesn't allow requests from your frontend domain.

**Solution**: Update your backend CORS configuration to include your frontend URL.

### Issue: 404 errors in production

**Cause**: Backend routes might not be properly configured or the API URL is incorrect.

**Solutions**:
1. Verify your backend is running and accessible
2. Check that your API URL includes the correct protocol (http/https)
3. Ensure your reverse proxy (if used) is configured correctly

## Examples

### Local Development
```
Frontend: http://localhost:3000
Backend:  http://localhost:5000
Config:   REACT_APP_API_URL=http://localhost:5000
```

### Server Deployment
```
Frontend: http://your-server.com
Backend:  http://your-server.com:5000
Config:   REACT_APP_API_URL=http://your-server.com:5000
```

### Same-Host with Reverse Proxy
```
Frontend: http://your-server.com/
Backend:  http://your-server.com/api
Config:   REACT_APP_API_URL= (empty, uses relative URLs)
```

### Docker Compose
```yaml
services:
  frontend:
    environment:
      - REACT_APP_API_URL=http://backend:5000
  backend:
    # backend service config
```
