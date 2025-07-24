import React from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Paper,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { 
  SchoolOutlined, 
  QuizOutlined 
} from '@mui/icons-material';

const GradeSelection = () => {
  const navigate = useNavigate();

  const handleGradeSelect = (grade) => {
    navigate(`/quiz/${grade}`);
  };

  const handleCompetitiveSelect = () => {
    navigate('/quiz/competitive');
  };

  const gradeGroups = [
    {
      title: 'Elementary School',
      subtitle: 'Foundation Building',
      grades: [1, 2, 3, 4, 5],
      color: 'success.main',
      bgColor: 'success.light',
    },
    {
      title: 'Middle School',
      subtitle: 'Core Concepts',
      grades: [6, 7, 8],
      color: 'warning.main',
      bgColor: 'warning.light',
    },
    {
      title: 'High School',
      subtitle: 'Advanced Mathematics',
      grades: [9, 10, 11, 12],
      color: 'error.main',
      bgColor: 'error.light',
    },
  ];

  const competitiveSection = {
    title: 'Competitive Exams',
    subtitle: 'Challenge Yourself',
    color: 'info.main',
    bgColor: 'info.light',
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <SchoolOutlined sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
        <Typography variant="h3" component="h1" gutterBottom>
          Choose Your Level
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Select the level you'd like to practice
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Competitive Exams Section */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 3,
              height: '100%',
              background: `linear-gradient(135deg, ${competitiveSection.bgColor} 0%, white 100%)`,
              border: `2px solid ${competitiveSection.color}`,
            }}
          >
            <Typography
              variant="h5"
              component="h2"
              gutterBottom
              sx={{ color: competitiveSection.color, fontWeight: 'bold' }}
            >
              {competitiveSection.title}
            </Typography>
            <Typography
              variant="subtitle1"
              color="text.secondary"
              sx={{ mb: 3 }}
            >
              {competitiveSection.subtitle}
            </Typography>

            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 3,
                    },
                  }}
                  onClick={handleCompetitiveSelect}
                >
                  <CardContent sx={{ textAlign: 'center', py: 2 }}>
                    <QuizOutlined 
                      sx={{ 
                        fontSize: 32, 
                        color: competitiveSection.color, 
                        mb: 1 
                      }} 
                    />
                    <Typography
                      variant="h6"
                      component="div"
                      sx={{ color: competitiveSection.color, fontWeight: 'bold' }}
                    >
                      Word Problems
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Complex Problems
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Grade Groups */}
        {gradeGroups.map((group) => (
          <Grid item xs={12} md={3} key={group.title}>
            <Paper
              sx={{
                p: 3,
                height: '100%',
                background: `linear-gradient(135deg, ${group.bgColor} 0%, white 100%)`,
                border: `2px solid ${group.color}`,
              }}
            >
              <Typography
                variant="h5"
                component="h2"
                gutterBottom
                sx={{ color: group.color, fontWeight: 'bold' }}
              >
                {group.title}
              </Typography>
              <Typography
                variant="subtitle1"
                color="text.secondary"
                sx={{ mb: 3 }}
              >
                {group.subtitle}
              </Typography>

              <Grid container spacing={2}>
                {group.grades.map((grade) => (
                  <Grid item xs={6} key={grade}>
                    <Card
                      sx={{
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                        '&:hover': {
                          transform: 'translateY(-4px)',
                          boxShadow: 3,
                        },
                      }}
                      onClick={() => handleGradeSelect(grade)}
                    >
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography
                          variant="h4"
                          component="div"
                          sx={{ color: group.color, fontWeight: 'bold' }}
                        >
                          {grade}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Grade {grade}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Paper sx={{ p: 4, bgcolor: 'primary.main', color: 'white' }}>
          <Typography variant="h6" gutterBottom>
            Not sure which grade to choose?
          </Typography>
          <Typography variant="body1" sx={{ mb: 2 }}>
            Start with a grade level where you feel comfortable and work your way up!
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => handleGradeSelect(1)}
              sx={{
                bgcolor: 'white',
                color: 'primary.main',
                '&:hover': {
                  bgcolor: 'grey.100',
                },
              }}
            >
              Start with Grade 1
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/math-test')}
              sx={{
                borderColor: 'white',
                color: 'white',
                '&:hover': {
                  borderColor: 'white',
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              View Math Examples
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default GradeSelection;
