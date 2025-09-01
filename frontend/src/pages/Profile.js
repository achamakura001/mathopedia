import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Paper,
  Chip,
  LinearProgress,
  Avatar,
  Alert,
  Tab,
  Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Badge,
} from '@mui/material';
import {
  PersonOutlined,
  TrendingUpOutlined,
  EmojiEventsOutlined,
  CalendarTodayOutlined,
  SchoolOutlined,
  CheckCircleOutlined,
  CancelOutlined,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { profileService, answerService } from '../services/questionService';
import LoadingSpinner from '../components/LoadingSpinner';

const Profile = () => {
  const { user } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [profileData, setProfileData] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const [recentAnswers, setRecentAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProfileData();
  }, []);

  const loadProfileData = async () => {
    try {
      const [profileResponse, achievementsResponse, answersResponse] = await Promise.all([
        profileService.getProfile(),
        profileService.getAchievements(),
        answerService.getAnswerHistory(1, 10),
      ]);
      
      setProfileData(profileResponse);
      setAchievements(achievementsResponse.achievements || []);
      setRecentAnswers(answersResponse.answers || []);
    } catch (err) {
      setError('Failed to load profile data');
      console.error('Profile error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  if (loading) {
    return <LoadingSpinner message="Loading your profile..." />;
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  const stats = profileData?.stats || {};
  const gradePerformance = profileData?.grade_performance || [];
  const dailyProgress = profileData?.daily_progress || [];

  // Calculate recent performance (last 7 days)
  const recentProgress = dailyProgress.slice(-7);
  const recentTotal = recentProgress.reduce((sum, day) => sum + day.questions_answered, 0);
  const recentCorrect = recentProgress.reduce((sum, day) => sum + day.correct_answers, 0);
  const recentAccuracy = recentTotal > 0 ? Math.round((recentCorrect / recentTotal) * 100) : 0;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Profile Header */}
      <Paper sx={{ p: 4, mb: 4, background: 'var(--gradient-primary)', color: 'white' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
          <Avatar
            sx={{
              width: 80,
              height: 80,
              bgcolor: 'white',
              color: 'primary.main',
              fontSize: '2rem',
              fontWeight: 'bold',
            }}
          >
            {user?.first_name?.[0]?.toUpperCase()}{user?.last_name?.[0]?.toUpperCase()}
          </Avatar>
          <Box>
            <Typography variant="h4" component="h1" gutterBottom>
              {user?.first_name} {user?.last_name}
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              {user?.email}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              Member since {new Date(user?.created_at).toLocaleDateString()}
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Overview" icon={<PersonOutlined />} />
          <Tab label="Performance" icon={<TrendingUpOutlined />} />
          <Tab label="Achievements" icon={<EmojiEventsOutlined />} />
          <Tab label="Recent Activity" icon={<CalendarTodayOutlined />} />
        </Tabs>
      </Box>

      {/* Tab Content */}
      {tabValue === 0 && (
        // Overview Tab
        <Grid container spacing={3}>
          {/* Overall Stats */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Overall Statistics
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography>Total Questions:</Typography>
                    <Typography fontWeight="bold">{stats.total_questions_answered || 0}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography>Correct Answers:</Typography>
                    <Typography fontWeight="bold">{stats.correct_answers || 0}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography>Overall Accuracy:</Typography>
                    <Chip
                      label={`${stats.overall_accuracy || 0}%`}
                      color={stats.overall_accuracy >= 80 ? 'success' : stats.overall_accuracy >= 60 ? 'warning' : 'error'}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography>Study Streak:</Typography>
                    <Typography fontWeight="bold">{stats.current_streak || 0} days</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography>Total Study Days:</Typography>
                    <Typography fontWeight="bold">{stats.total_study_days || 0}</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Recent Performance */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Last 7 Days Performance
                </Typography>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <Typography variant="h3" color="primary.main">
                    {recentAccuracy}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Recent Accuracy
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="body2">
                    Questions: {recentTotal}
                  </Typography>
                  <Typography variant="body2">
                    Correct: {recentCorrect}
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={recentAccuracy}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {tabValue === 1 && (
        // Performance Tab
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Grade-wise Performance
                </Typography>
                {gradePerformance.length > 0 ? (
                  <Grid container spacing={2}>
                    {gradePerformance.map((grade) => (
                      <Grid item xs={12} sm={6} md={4} key={grade.grade}>
                        <Paper sx={{ p: 2, textAlign: 'center' }}>
                          <SchoolOutlined sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                          <Typography variant="h6">{grade.grade_display}</Typography>
                          <Typography variant="h4" color="primary.main">
                            {grade.accuracy}%
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {grade.correct_answers}/{grade.total_questions} correct
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={grade.accuracy}
                            sx={{ mt: 1, height: 6, borderRadius: 3 }}
                          />
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                ) : (
                  <Alert severity="info">
                    No grade performance data yet. Start practicing to see your progress!
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {tabValue === 2 && (
        // Achievements Tab
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Your Achievements
                </Typography>
                {achievements.length > 0 ? (
                  <Grid container spacing={2}>
                    {achievements.map((achievement, index) => (
                      <Grid item xs={12} sm={6} md={4} key={index}>
                        <Paper
                          sx={{
                            p: 2,
                            textAlign: 'center',
                            bgcolor: achievement.earned ? 'success.light' : 'grey.100',
                            color: achievement.earned ? 'success.contrastText' : 'text.secondary',
                          }}
                        >
                          <Badge
                            badgeContent={achievement.earned ? <CheckCircleOutlined /> : null}
                            color="success"
                          >
                            <EmojiEventsOutlined
                              sx={{
                                fontSize: 48,
                                color: achievement.earned ? 'warning.main' : 'grey.400',
                              }}
                            />
                          </Badge>
                          <Typography variant="h6" sx={{ mt: 1 }}>
                            {achievement.title}
                          </Typography>
                          <Typography variant="body2">
                            {achievement.description}
                          </Typography>
                          <Chip
                            label={achievement.type}
                            size="small"
                            sx={{ mt: 1 }}
                            color={achievement.earned ? 'success' : 'default'}
                          />
                        </Paper>
                      </Grid>
                    ))}
                  </Grid>
                ) : (
                  <Alert severity="info">
                    Keep practicing to earn achievements!
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {tabValue === 3 && (
        // Recent Activity Tab
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Answers
                </Typography>
                {recentAnswers.length > 0 ? (
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Date</TableCell>
                          <TableCell>Grade</TableCell>
                          <TableCell>Complexity</TableCell>
                          <TableCell>Topic</TableCell>
                          <TableCell>Result</TableCell>
                          <TableCell>Your Answer</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {recentAnswers.map((answer) => (
                          <TableRow key={answer.id}>
                            <TableCell>
                              {new Date(answer.answered_at).toLocaleDateString()}
                            </TableCell>
                            <TableCell>
                              Grade {answer.question?.grade_level}
                            </TableCell>
                            <TableCell>
                              {answer.question?.complexity}
                            </TableCell>
                            <TableCell>
                              {answer.question?.topic}
                            </TableCell>
                            <TableCell>
                              {answer.is_correct ? (
                                <Chip
                                  icon={<CheckCircleOutlined />}
                                  label="Correct"
                                  color="success"
                                  size="small"
                                />
                              ) : (
                                <Chip
                                  icon={<CancelOutlined />}
                                  label="Incorrect"
                                  color="error"
                                  size="small"
                                />
                              )}
                            </TableCell>
                            <TableCell>{answer.user_answer}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                ) : (
                  <Alert severity="info">
                    No recent activity. Start practicing to see your answers here!
                  </Alert>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  );
};

export default Profile;
