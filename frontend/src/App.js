import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import { useAuth } from './contexts/AuthContext';

// Components
import Navbar from './components/Navbar';
import LoadingSpinner from './components/LoadingSpinner';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Quiz from './pages/Quiz';
import Profile from './pages/Profile';
import GradeSelection from './pages/GradeSelection';
import AdminPanel from './pages/AdminPanel';
import MathTest from './pages/MathTest';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Box sx={{ flex: 1, pt: 2 }}>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<Home />} />
          <Route 
            path="/login" 
            element={user ? <Navigate to="/dashboard" /> : <Login />} 
          />
          <Route 
            path="/register" 
            element={user ? <Navigate to="/dashboard" /> : <Register />} 
          />
          
          {/* Protected routes */}
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/grade-selection" 
            element={user ? <GradeSelection /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/quiz/:grade" 
            element={user ? <Quiz /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/profile" 
            element={user ? <Profile /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/admin" 
            element={user && user.is_admin ? <AdminPanel /> : <Navigate to="/dashboard" />} 
          />
          <Route 
            path="/math-test" 
            element={<MathTest />} 
          />
          
          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;
