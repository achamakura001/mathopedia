import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  LinearProgress,
  Alert,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Paper,
  Fade,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import {
  CheckCircleOutlined,
  CancelOutlined,
  QuizOutlined,
  NavigateNextOutlined,
  NavigateBeforeOutlined,
  EmojiEventsOutlined,
} from '@mui/icons-material';
import { questionService, answerService } from '../services/questionService';
import LoadingSpinner from '../components/LoadingSpinner';
import MathKeyboard from '../components/MathKeyboard';
import { MathText } from '../components/MathRenderer';

const Quiz = () => {
  const { grade } = useParams();
  const navigate = useNavigate();
  
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [showResult, setShowResult] = useState(false);
  const [currentResult, setCurrentResult] = useState(null);
  const [quizComplete, setQuizComplete] = useState(false);
  const [quizSummary, setQuizSummary] = useState(null);
  const [mathKeyboardOpen, setMathKeyboardOpen] = useState(false);

  const loadQuestions = useCallback(async () => {
    try {
      setLoading(true);
      let response;
      
      if (grade === 'competitive') {
        response = await questionService.getCompetitiveQuestions();
      } else {
        response = await questionService.getQuestionsForGrade(parseInt(grade));
      }
      
      setQuestions(response.questions);
      
      if (response.questions.length === 0) {
        setError('No more questions available for this level. Try a different level!');
      }
    } catch (err) {
      setError('Failed to load questions. Please try again.');
      console.error('Question loading error:', err);
    } finally {
      setLoading(false);
    }
  }, [grade]);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  const handleAnswerSubmit = async () => {
    if (!userAnswer.trim()) {
      alert('Please enter an answer before submitting.');
      return;
    }

    setSubmitting(true);
    try {
      const currentQuestion = questions[currentQuestionIndex];
      const result = await answerService.submitAnswer(currentQuestion.id, userAnswer, currentQuestion.test_identifier);
      
      setCurrentResult(result);
      setShowResult(true);
      
      // Store the answer
      const answerData = {
        questionId: currentQuestion.id,
        userAnswer: userAnswer,
        isCorrect: result.is_correct,
        correctAnswer: result.correct_answer,
        explanation: result.explanation,
      };
      
      setAnswers([...answers, answerData]);
      
    } catch (err) {
      setError('Failed to submit answer. Please try again.');
      console.error('Answer submission error:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    setShowResult(false);
    setCurrentResult(null);
    setUserAnswer('');
    setMathKeyboardOpen(false); // Collapse math keyboard when moving to next question
    
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // Quiz completed
      const correctCount = answers.filter(a => a.isCorrect).length + (currentResult?.is_correct ? 1 : 0);
      const totalCount = questions.length;
      const accuracy = Math.round((correctCount / totalCount) * 100);
      
      setQuizSummary({
        correct: correctCount,
        total: totalCount,
        accuracy: accuracy,
        grade: parseInt(grade),
      });
      setQuizComplete(true);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
      // Load the previous answer if it exists
      const prevAnswer = answers[currentQuestionIndex - 1];
      if (prevAnswer) {
        setUserAnswer(prevAnswer.userAnswer);
      }
    }
  };

  const handleRetryQuiz = () => {
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setUserAnswer('');
    setAnswers([]);
    setShowResult(false);
    setCurrentResult(null);
    setQuizComplete(false);
    setQuizSummary(null);
    setError('');
    setMathKeyboardOpen(false);
    loadQuestions();
  };

  const handleMathKeyboardToggle = () => {
    setMathKeyboardOpen(!mathKeyboardOpen);
  };

  const handleSymbolSelect = (symbol) => {
    setUserAnswer(prev => prev + symbol);
  };

  const currentQuestion = questions[currentQuestionIndex];
  const progress = questions.length > 0 ? ((currentQuestionIndex + 1) / questions.length) * 100 : 0;
  const isAnswered = answers.some(a => a.questionId === currentQuestion?.id);

  if (loading) {
    return <LoadingSpinner message="Loading quiz questions..." />;
  }

  if (error && questions.length === 0) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button variant="contained" onClick={() => navigate('/grade-selection')}>
          Choose Different Grade
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      {/* Quiz Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <QuizOutlined sx={{ color: 'primary.main', mr: 1 }} />
          <Typography variant="h4" component="h1">
            {grade === 'competitive' ? 'Competitive Exams' : `Grade ${grade}`} Math Quiz
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Typography variant="body1">
            Question {currentQuestionIndex + 1} of {questions.length}
          </Typography>
          <Chip
            label={currentQuestion?.complexity || 'N/A'}
            color={
              currentQuestion?.complexity === 'easy' ? 'success' :
              currentQuestion?.complexity === 'medium' ? 'warning' : 'error'
            }
            size="small"
          />
          <Chip
            label={currentQuestion?.topic || 'Math'}
            variant="outlined"
            size="small"
          />
        </Box>
        
        <LinearProgress
          variant="determinate"
          value={progress}
          sx={{ height: 8, borderRadius: '4px' }}
        />
      </Box>

      {/* Question Card */}
      <Fade in={!showResult} timeout={300}>
        <Card sx={{ mb: 4, display: showResult ? 'none' : 'block' }}>
          <CardContent sx={{ p: 4 }}>
            <Box className="math-question" sx={{ mb: 3 }}>
              <MathText className="question-text">
                {currentQuestion?.question_text}
              </MathText>
            </Box>
            
            <TextField
              fullWidth
              label="Your Answer"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Enter your answer here..."
              multiline
              rows={3}
              sx={{ mt: 3, mb: 3 }}
              disabled={isAnswered}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  if (!isAnswered) {
                    handleAnswerSubmit();
                  }
                }
              }}
              onKeyDown={(e) => {
                // Open math keyboard with Ctrl+M or Cmd+M
                if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
                  e.preventDefault();
                  if (!isAnswered) {
                    handleMathKeyboardToggle();
                  }
                }
              }}
            />
            
            {/* Math Keyboard - Inline */}
            <MathKeyboard
              open={mathKeyboardOpen}
              onToggle={handleMathKeyboardToggle}
              onSymbolSelect={handleSymbolSelect}
            />
            
            <Typography variant="caption" color="text.secondary" sx={{ ml: 1, mb: 2, display: 'block' }}>
              💡 Tip: Use the math keyboard above or press Ctrl+M (Cmd+M on Mac) to access math symbols
            </Typography>
            
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Button
                startIcon={<NavigateBeforeOutlined />}
                onClick={handlePreviousQuestion}
                disabled={currentQuestionIndex === 0}
              >
                Previous
              </Button>
              
              <Button
                variant="contained"
                onClick={handleAnswerSubmit}
                disabled={submitting || isAnswered || !userAnswer.trim()}
                sx={{ minWidth: 120 }}
              >
                {submitting ? 'Submitting...' : 'Submit Answer'}
              </Button>
            </Box>
          </CardContent>
        </Card>
      </Fade>

      {/* Result Dialog */}
      <Dialog
        open={showResult}
        maxWidth="md"
        fullWidth
        onClose={() => {}}
        disableEscapeKeyDown
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {currentResult?.is_correct ? (
              <CheckCircleOutlined sx={{ color: 'success.main' }} />
            ) : (
              <CancelOutlined sx={{ color: 'error.main' }} />
            )}
            <Typography variant="h6">
              {currentResult?.is_correct ? 'Correct!' : 'Incorrect'}
            </Typography>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {!currentResult?.is_correct && (
            <Paper sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
              <Typography variant="h6" gutterBottom>
                Question:
              </Typography>
              <Box className="math-question">
                <MathText>
                  {questions[currentQuestionIndex]?.question_text}
                </MathText>
              </Box>
            </Paper>
          )}
          
          <Paper sx={{ p: 2, mb: 2, bgcolor: currentResult?.is_correct ? 'success.light' : 'error.light' }}>
            <Typography variant="body1" gutterBottom>
              <strong>Your Answer:</strong> <MathText>{currentResult?.user_answer}</MathText>
            </Typography>
            <Typography variant="body1" gutterBottom>
              <strong>Correct Answer:</strong> <MathText>{currentResult?.correct_answer}</MathText>
            </Typography>
          </Paper>
          
          <Typography variant="h6" gutterBottom>
            Explanation:
          </Typography>
          <Box className="math-explanation">
            <MathText>
              {currentResult?.explanation}
            </MathText>
          </Box>
        </DialogContent>
        
        <DialogActions>
          <Button
            variant="contained"
            onClick={handleNextQuestion}
            startIcon={<NavigateNextOutlined />}
          >
            {currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Finish Quiz'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Quiz Complete Dialog */}
      <Dialog
        open={quizComplete}
        maxWidth="sm"
        fullWidth
        onClose={() => {}}
        disableEscapeKeyDown
      >
        <DialogTitle>
          <Box sx={{ textAlign: 'center' }}>
            <EmojiEventsOutlined sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
            <Typography variant="h5">Quiz Complete!</Typography>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h3" component="div" color="primary.main" gutterBottom>
              {quizSummary?.accuracy}%
            </Typography>
            <Typography variant="body1" gutterBottom>
              You got <strong>{quizSummary?.correct}</strong> out of <strong>{quizSummary?.total}</strong> questions correct!
            </Typography>
            
            <Box sx={{ mt: 3 }}>
              {quizSummary?.accuracy >= 80 && (
                <Alert severity="success" sx={{ mb: 2 }}>
                  Excellent work! You're mastering {grade === 'competitive' ? 'competitive level' : `Grade ${grade}`} math!
                </Alert>
              )}
              {quizSummary?.accuracy >= 60 && quizSummary?.accuracy < 80 && (
                <Alert severity="info" sx={{ mb: 2 }}>
                  Good job! Keep practicing to improve your score.
                </Alert>
              )}
              {quizSummary?.accuracy < 60 && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  Keep practicing! Review the explanations to improve.
                </Alert>
              )}
            </Box>
          </Box>
        </DialogContent>
        
        <DialogActions sx={{ justifyContent: 'space-between', p: 3 }}>
          <Button
            variant="outlined"
            onClick={() => navigate('/dashboard')}
          >
            Back to Dashboard
          </Button>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button
              variant="outlined"
              onClick={() => navigate('/grade-selection')}
            >
              Try Different Grade
            </Button>
            <Button
              variant="contained"
              onClick={handleRetryQuiz}
            >
              Practice More
            </Button>
          </Box>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Quiz;
