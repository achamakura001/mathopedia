# Frontend Setup Guide

## Prerequisites

- Node.js 16 or higher
- npm or yarn package manager

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` if needed:
   ```env
   REACT_APP_API_URL=http://localhost:5000
   ```

## Running the Application

1. **Start the development server:**
   ```bash
   npm start
   # or
   yarn start
   ```
   
   The application will be available at `http://localhost:3000`

2. **The app will automatically proxy API requests to the backend at `http://localhost:5000`**

## Building for Production

1. **Create production build:**
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Serve the built files:**
   ```bash
   npm install -g serve
   serve -s build
   ```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Create production build
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App (not recommended)

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── Navbar.js       # Navigation bar
│   └── LoadingSpinner.js # Loading component
├── contexts/           # React contexts
│   └── AuthContext.js  # Authentication context
├── pages/              # Page components
│   ├── Home.js         # Landing page
│   ├── Login.js        # Login page
│   ├── Register.js     # Registration page
│   ├── Dashboard.js    # User dashboard
│   ├── GradeSelection.js # Grade selection
│   ├── Quiz.js         # Quiz interface
│   └── Profile.js      # User profile
├── services/           # API services
│   ├── api.js          # Axios configuration
│   └── questionService.js # Question/answer services
├── App.js              # Main app component
└── index.js            # Entry point
```

## Features

### Authentication
- User registration with validation
- Login with JWT tokens
- Automatic token refresh
- Protected routes

### Quiz System
- Grade-based question selection
- Real-time answer submission
- Detailed explanations
- Progress tracking

### Dashboard
- Personal statistics
- Daily progress
- Recent activity
- Quick actions

### Profile
- Comprehensive user stats
- Achievement system
- Performance analytics
- Activity history

## Customization

### Theming
Modify the theme in `src/index.js`:
```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#your-color',
    },
    // ... other theme options
  },
});
```

### Adding New Pages
1. Create component in `src/pages/`
2. Add route in `src/App.js`
3. Add navigation link if needed

### API Integration
Add new services in `src/services/` following the pattern in `questionService.js`

## Deployment

### Static Hosting (Netlify, Vercel)
1. Build the project: `npm run build`
2. Upload the `build` folder to your hosting provider
3. Configure environment variables for API URL

### Docker
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Troubleshooting

### Common Issues

1. **CORS errors:** Make sure the backend is running and CORS is configured
2. **API connection issues:** Check the proxy configuration in `package.json`
3. **Build errors:** Clear node_modules and reinstall dependencies
