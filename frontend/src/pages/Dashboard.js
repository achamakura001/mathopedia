import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  LinearProgress,
  Chip,
  Paper,
  Alert,
} from '@mui/material';
import { Link } from 'react-router-dom';
import {
  TrendingUpOutlined,
  QuizOutlined,
  EmojiEventsOutlined,
  CalendarTodayOutlined,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { profileService, answerService } from '../services/questionService';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const { user } = useAuth();
  const [profileData, setProfileData] = useState(null);
  const [recentStats, setRecentStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [profileResponse, statsResponse] = await Promise.all([
        profileService.getProfile(),
        answerService.getAnswerStats(),
      ]);
      
      setProfileData(profileResponse);
      setRecentStats(statsResponse);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading your dashboard..." />;
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  const stats = profileData?.stats || {};
  const todayProgress = profileData?.daily_progress?.slice(-1)[0];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Welcome Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Welcome back, {user?.first_name}! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's your learning progress and recent activity
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <QuizOutlined sx={{ color: 'primary.main', mr: 1 }} />
                <Typography variant="h6" component="div">
                  Total Questions
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="primary.main">
                {stats.total_questions_answered || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Questions answered
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpOutlined sx={{ color: 'success.main', mr: 1 }} />
                <Typography variant="h6" component="div">
                  Accuracy
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="success.main">
                {stats.overall_accuracy || 0}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Overall accuracy
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CalendarTodayOutlined sx={{ color: 'warning.main', mr: 1 }} />
                <Typography variant="h6" component="div">
                  Study Streak
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="warning.main">
                {stats.current_streak || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Days in a row
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <EmojiEventsOutlined sx={{ color: 'secondary.main', mr: 1 }} />
                <Typography variant="h6" component="div">
                  Study Days
                </Typography>
              </Box>
              <Typography variant="h4" component="div" color="secondary.main">
                {stats.total_study_days || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total active days
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Today's Progress */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Today's Progress
              </Typography>
              {todayProgress ? (
                <Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">
                      Questions Answered: {todayProgress.questions_answered}
                    </Typography>
                    <Typography variant="body2">
                      Accuracy: {todayProgress.accuracy}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={Math.min(todayProgress.questions_answered * 10, 100)}
                    sx={{ mb: 2 }}
                  />
                  <Typography variant="body2" color="text.secondary">
                    Keep going! Try to answer at least 10 questions today.
                  </Typography>
                </Box>
              ) : (
                <Box>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    You haven't answered any questions today yet.
                  </Typography>
                  <Button
                    variant="contained"
                    component={Link}
                    to="/grade-selection"
                    startIcon={<QuizOutlined />}
                  >
                    Start Practicing
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Grade Performance */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Grade Performance
              </Typography>
              {profileData?.grade_performance?.length > 0 ? (
                <Box>
                  {profileData.grade_performance.slice(0, 5).map((grade) => (
                    <Box key={grade.grade} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">
                          Grade {grade.grade}
                        </Typography>
                        <Chip
                          label={`${grade.accuracy}%`}
                          size="small"
                          color={grade.accuracy >= 80 ? 'success' : grade.accuracy >= 60 ? 'warning' : 'error'}
                        />
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={grade.accuracy}
                        sx={{ mb: 1 }}
                      />
                      <Typography variant="caption" color="text.secondary">
                        {grade.correct_answers}/{grade.total_questions} correct
                      </Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No grade performance data yet. Start practicing to see your progress!
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                component={Link}
                to="/grade-selection"
                startIcon={<QuizOutlined />}
              >
                Practice Questions
              </Button>
              <Button
                variant="outlined"
                component={Link}
                to="/profile"
                startIcon={<TrendingUpOutlined />}
              >
                View Detailed Progress
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
