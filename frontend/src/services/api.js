import axios from 'axios';

// Function to determine the API base URL
const getApiBaseUrl = () => {
  // If explicitly set via environment variable, use that (including empty string)
  if (process.env.REACT_APP_API_URL !== undefined) {
    return process.env.REACT_APP_API_URL;
  }
  
  // For production builds, try to auto-detect the host
  if (process.env.NODE_ENV === 'production') {
    // If running on the same host as backend, use relative URLs
    // This works when both frontend and backend are served from same domain
    return '';
  }
  
  // Development: try to detect if we're running on a different host
  if (typeof window !== 'undefined') {
    const currentHost = window.location.hostname;
    const currentProtocol = window.location.protocol;
    
    // If not localhost, assume backend is on same host with port 5000
    if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
      return `${currentProtocol}//${currentHost}:5000`;
    }
  }
  
  // Development fallback for localhost
  return 'http://localhost:5000';
};

const API_BASE_URL = getApiBaseUrl();

// Debug logging for API configuration
console.log('🔧 API Configuration:', {
  NODE_ENV: process.env.NODE_ENV,
  REACT_APP_API_URL: process.env.REACT_APP_API_URL,
  calculatedBaseURL: API_BASE_URL,
  currentLocation: typeof window !== 'undefined' ? window.location.href : 'N/A'
});

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
