# Deployment Guide - Fixing API Configuration Issues

This guide addresses the common issue where "API calls go to localhost instead of the port or hostname used to open the frontend page."

## The Problem

When deploying Mathopedia to different servers or environments, users often face issues where:
- Frontend loads correctly on `http://your-server:3000`
- But API calls still go to `http://localhost:5000` instead of `http://your-server:5000`
- This causes "Connection refused" or CORS errors

## The Solution

The frontend now includes smart API configuration that adapts to different deployment scenarios automatically.

## Quick Fix

### ✅ NEW: Auto-Detection (Recommended)

**No configuration needed!** The app now automatically detects your deployment environment.

1. **Remove any existing .env file** (if it contains localhost):
   ```bash
   cd frontend
   rm .env
   npm start
   ```

2. **How it works**:
   - Accesses via IP (`http://192.168.1.100:3000`) → API calls go to `http://192.168.1.100:5000`
   - Accesses via localhost → API calls go to `http://localhost:5000`
   - Production builds → Uses relative URLs

### Manual Configuration

### Method 1: Automatic Setup (Recommended)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Run the setup script:
   ```bash
   ./setup-env.sh
   ```

3. Choose your deployment type and follow the prompts.

4. Restart your application:
   ```bash
   npm start
   ```

### Method 2: Manual Configuration

1. Create a `.env` file in the `frontend` directory:
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. Edit the `.env` file based on your deployment:

   **For development:**
   ```
   REACT_APP_API_URL=http://localhost:5000
   ```

   **For production with custom server:**
   ```
   REACT_APP_API_URL=http://your-server-ip:5000
   ```

   **For same-host deployment:**
   ```
   # Leave this empty or comment it out
   # REACT_APP_API_URL=
   ```

3. Restart your application.

## Deployment Scenarios

### Scenario 1: Development
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`
- Configuration: `REACT_APP_API_URL=http://localhost:5000`

### Scenario 2: Different Server
- Frontend: `http://192.168.1.100:3000`
- Backend: `http://192.168.1.100:5000`
- Configuration: `REACT_APP_API_URL=http://192.168.1.100:5000`

### Scenario 3: Same Server, Different Ports
- Frontend: `http://myserver.com:3000`
- Backend: `http://myserver.com:5000`
- Configuration: `REACT_APP_API_URL=http://myserver.com:5000`

### Scenario 4: Reverse Proxy (Same Host)
- Frontend: `http://myserver.com/`
- Backend: `http://myserver.com/api`
- Configuration: Leave `REACT_APP_API_URL` empty (uses relative URLs)

### Scenario 5: Docker Deployment
- Configuration: `REACT_APP_API_URL=http://backend:5000`

## Troubleshooting

### Issue: Still getting localhost errors

**Check 1:** Verify your `.env` file exists and is in the correct location:
```bash
ls -la frontend/.env
```

**Check 2:** Verify the content of your `.env` file:
```bash
cat frontend/.env
```

**Check 3:** Restart the application after changing `.env`:
```bash
# Stop the application (Ctrl+C)
# Then restart:
npm start
```

### Issue: CORS errors

Update your backend CORS configuration to allow requests from your frontend domain.

In `backend/app/__init__.py`, ensure CORS allows your frontend URL:
```python
CORS(app, origins=["http://your-frontend-url:3000"])
```

### Issue: 404 errors

1. Verify your backend is running and accessible
2. Test backend directly: `curl http://your-backend:5000/api/auth/login`
3. Check backend logs for errors

## Testing Your Configuration

Run the configuration test:
```bash
cd frontend
node test-api-config.js
```

This will verify that your API configuration logic is working correctly.

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API base URL | `http://localhost:5000` |
| Not set | Uses smart defaults | Development: localhost, Production: relative URLs |
| Empty string | Forces relative URLs | Good for same-host deployments |

## Advanced Configuration

### Docker Compose Example

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:5000
    depends_on:
      - backend
  
  backend:
    build: ./backend
    ports:
      - "5000:5000"
```

### Nginx Reverse Proxy Example

```nginx
server {
    listen 80;
    server_name myserver.com;
    
    location / {
        proxy_pass http://localhost:3000;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

With this setup, use: `REACT_APP_API_URL=` (empty, for relative URLs)

## Production Deployment

### Build Configuration

For production builds, the app automatically uses relative URLs if no explicit API URL is set:

```bash
# This will use relative URLs in production
npm run build

# This will use a specific API URL
REACT_APP_API_URL=https://api.myserver.com npm run build
```

### Static File Serving

When serving the built files statically, ensure your web server proxies API requests to your backend:

```bash
# Build the frontend
npm run build

# Serve with a static server
npm install -g serve
serve -s build -l 3000
```

Make sure your reverse proxy forwards `/api/*` requests to your backend.

## Getting Help

If you're still experiencing issues:

1. Check the browser console for error messages
2. Check the network tab to see where requests are being sent
3. Verify your backend is accessible from your frontend server
4. Test the API endpoints directly with curl or Postman

The new configuration system should handle most deployment scenarios automatically, but these troubleshooting steps will help identify any remaining issues.
