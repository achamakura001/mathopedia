import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  Link as MuiLink,
  InputAdornment,
  IconButton,
  Grid,
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { Visibility, VisibilityOff, PersonAddOutlined } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear error when user starts typing
    if (error) setError('');
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!validateForm()) {
      setLoading(false);
      return;
    }

    const result = await register(
      formData.firstName,
      formData.lastName,
      formData.email,
      formData.password
    );
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper
          sx={{
            p: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <PersonAddOutlined sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom>
            Create Account
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Join Mathopedia and start your learning journey
          </Typography>

          {error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  name="firstName"
                  label="First Name"
                  value={formData.firstName}
                  onChange={handleChange}
                  fullWidth
                  required
                  autoComplete="given-name"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  name="lastName"
                  label="Last Name"
                  value={formData.lastName}
                  onChange={handleChange}
                  fullWidth
                  required
                  autoComplete="family-name"
                />
              </Grid>
            </Grid>
            
            <TextField
              name="email"
              type="email"
              label="Email Address"
              value={formData.email}
              onChange={handleChange}
              fullWidth
              required
              margin="normal"
              autoComplete="email"
            />
            
            <TextField
              name="password"
              type={showPassword ? 'text' : 'password'}
              label="Password"
              value={formData.password}
              onChange={handleChange}
              fullWidth
              required
              margin="normal"
              autoComplete="new-password"
              helperText="Password must be at least 6 characters long"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              name="confirmPassword"
              type={showConfirmPassword ? 'text' : 'password'}
              label="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              fullWidth
              required
              margin="normal"
              autoComplete="new-password"
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle confirm password visibility"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      edge="end"
                    >
                      {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={loading}
              sx={{ mt: 3, mb: 2, py: 1.5 }}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </Button>

            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body2">
                Already have an account?{' '}
                <MuiLink component={Link} to="/login" variant="body2">
                  Sign in here
                </MuiLink>
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Register;
