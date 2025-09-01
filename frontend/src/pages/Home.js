import React from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Paper,
} from '@mui/material';
import { Link } from 'react-router-dom';
import {
  SchoolOutlined,
  TrendingUpOutlined,
  EmojiEventsOutlined,
  GroupOutlined,
} from '@mui/icons-material';

const Home = () => {
  const features = [
    {
      icon: <SchoolOutlined sx={{ fontSize: 60, color: 'primary.main' }} />,
      title: 'Grade-Specific Practice',
      description: 'Tailored math questions for grades 1-12 with appropriate difficulty levels.',
    },
    {
      icon: <TrendingUpOutlined sx={{ fontSize: 60, color: 'secondary.main' }} />,
      title: 'Progress Tracking',
      description: 'Monitor your daily progress and see your improvement over time.',
    },
    {
      icon: <EmojiEventsOutlined sx={{ fontSize: 60, color: 'warning.main' }} />,
      title: 'Achievements',
      description: 'Earn badges and achievements as you master different math concepts.',
    },
    {
      icon: <GroupOutlined sx={{ fontSize: 60, color: 'info.main' }} />,
      title: 'Adaptive Learning',
      description: 'Questions adapt to your skill level for optimal learning experience.',
    },
  ];

  return (
    <Container maxWidth="lg">
      {/* Hero Section */}
      <Box
        sx={{
          py: 8,
          textAlign: 'center',
          background: 'var(--gradient-primary)',
          color: 'white',
          borderRadius: 2,
          mb: 6,
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
          Welcome to Mathopedia
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom sx={{ mb: 4 }}>
          Learn & Practice Math with Confidence: Grades 1-12
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
          <Button
            variant="contained"
            size="large"
            component={Link}
            to="/register"
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              '&:hover': {
                bgcolor: 'grey.100',
              },
            }}
          >
            Get Started
          </Button>
          <Button
            variant="outlined"
            size="large"
            component={Link}
            to="/login"
            sx={{
              borderColor: 'white',
              color: 'white',
              '&:hover': {
                borderColor: 'white',
                bgcolor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            Sign In
          </Button>
        </Box>
      </Box>

      {/* Features Section */}
      <Box sx={{ mb: 8 }}>
        <Typography variant="h4" component="h2" textAlign="center" gutterBottom>
          Why Choose Mathopedia?
        </Typography>
        <Typography
          variant="h6"
          component="p"
          textAlign="center"
          color="text.secondary"
          sx={{ mb: 6 }}
        >
          Discover the features that make learning math engaging and effective
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  textAlign: 'center',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1, p: 3 }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" component="h3" gutterBottom>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* How It Works Section */}
      <Paper sx={{ p: 6, mb: 8, bgcolor: 'background.paper' }}>
        <Typography variant="h4" component="h2" textAlign="center" gutterBottom>
          How It Works
        </Typography>
        <Grid container spacing={4} sx={{ mt: 2 }}>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h2"
                component="div"
                sx={{
                  color: 'primary.main',
                  fontWeight: 'bold',
                  mb: 2,
                }}
              >
                1
              </Typography>
              <Typography variant="h6" gutterBottom>
                Choose Your Grade
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Select your current grade level from 1st to 12th grade
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h2"
                component="div"
                sx={{
                  color: 'secondary.main',
                  fontWeight: 'bold',
                  mb: 2,
                }}
              >
                2
              </Typography>
              <Typography variant="h6" gutterBottom>
                Practice & Learn
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Answer questions tailored to your level with detailed explanations
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h2"
                component="div"
                sx={{
                  color: 'success.main',
                  fontWeight: 'bold',
                  mb: 2,
                }}
              >
                3
              </Typography>
              <Typography variant="h6" gutterBottom>
                Track Progress
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Monitor your daily progress and celebrate achievements
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* CTA Section */}
      <Box
        sx={{
          textAlign: 'center',
          py: 6,
          px: 4,
          bgcolor: 'primary.main',
          color: 'white',
          borderRadius: 2,
          mb: 4,
        }}
      >
        <Typography variant="h4" component="h2" gutterBottom>
          Ready to Start Learning?
        </Typography>
        <Typography variant="h6" component="p" sx={{ mb: 4 }}>
          Join thousands of students improving their math skills every day
        </Typography>
        <Button
          variant="contained"
          size="large"
          component={Link}
          to="/register"
          sx={{
            bgcolor: 'white',
            color: 'primary.main',
            '&:hover': {
              bgcolor: 'grey.100',
            },
          }}
        >
          Start Learning Now
        </Button>
      </Box>
    </Container>
  );
};

export default Home;
