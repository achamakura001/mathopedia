import React, { useState, useEffect, useCallback } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Alert,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  AdminPanelSettings as AdminIcon,
  School as SchoolIcon,
  People as PeopleIcon,
  AutoAwesome as GenerateIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../services/api';

const AdminPanel = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [topics, setTopics] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Topic dialog states
  const [topicDialogOpen, setTopicDialogOpen] = useState(false);
  const [editingTopic, setEditingTopic] = useState(null);
  const [topicForm, setTopicForm] = useState({
    topic: '',
    skill: '',
    grade_level: ''
  });
  
  // Question generation dialog states
  const [generateDialogOpen, setGenerateDialogOpen] = useState(false);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [generationForm, setGenerationForm] = useState({
    complexity: 'easy',
    count: 5,
    provider: 'ollama'
  });
  const [generating, setGenerating] = useState(false);
  
  // Filter states
  const [selectedGrade, setSelectedGrade] = useState('');
  
  useEffect(() => {
    if (!user || !user.is_admin) {
      navigate('/dashboard');
      return;
    }
    
    loadData();
  }, [user, navigate]);

  const loadTopics = useCallback(async () => {
    try {
      const url = selectedGrade 
        ? `/admin/topics?grade_level=${selectedGrade}`
        : '/admin/topics';
        
      console.log('Loading topics from:', url);
      const response = await api.get(url);
      
      console.log('Topics response status:', response.status);
      console.log('Topics response headers:', response.headers);
      console.log('Topics data received:', response.data);
      setTopics(response.data.topics);
    } catch (error) {
      console.error('Topics loading error:', error);
      if (error.response) {
        console.error('Error response data:', error.response.data);
        console.error('Error response status:', error.response.status);
        setError(`Failed to load topics: ${error.response.status} ${error.response.data.error || error.response.statusText}`);
      } else {
        setError(`Failed to load topics: ${error.message}`);
      }
    }
  }, [selectedGrade]);

  const loadUsers = useCallback(async () => {
    try {
      console.log('Loading users...');
      const response = await api.get('/admin/users');
      
      console.log('Users response status:', response.status);
      console.log('Users data received:', response.data);
      setUsers(response.data.users);
    } catch (error) {
      console.error('Users loading error:', error);
      if (error.response) {
        console.error('Users API error:', error.response.status, error.response.data);
        setError(`Failed to load users: ${error.response.status} ${error.response.data.error || error.response.statusText}`);
      } else {
        setError(`Failed to load users: ${error.message}`);
      }
    }
  }, []);

  // Reload topics when grade filter changes
  useEffect(() => {
    if (user && user.is_admin) {
      loadTopics();
    }
  }, [selectedGrade, user, loadTopics]);
  
  const loadData = async () => {
    try {
      setLoading(true);
      console.log('Loading admin data...');
      await Promise.all([loadTopics(), loadUsers()]);
      console.log('Admin data loaded successfully');
    } catch (error) {
      console.error('Error loading admin data:', error);
      setError(`Failed to load admin data: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCreateTopic = () => {
    setEditingTopic(null);
    setTopicForm({ topic: '', skill: '', grade_level: '' });
    setTopicDialogOpen(true);
  };
  
  const handleEditTopic = (topic) => {
    setEditingTopic(topic);
    setTopicForm({
      topic: topic.topic,
      skill: topic.skill,
      grade_level: String(topic.grade_level)
    });
    setTopicDialogOpen(true);
  };
  
  const handleSaveTopic = async () => {
    try {
      let response;
      
      if (editingTopic) {
        response = await api.put(`/admin/topics/${editingTopic.id}`, topicForm);
      } else {
        response = await api.post('/admin/topics', topicForm);
      }
      
      setSuccess(`Topic ${editingTopic ? 'updated' : 'created'} successfully`);
      setTopicDialogOpen(false);
      loadTopics();
    } catch (error) {
      if (error.response) {
        setError(error.response.data.error || 'Failed to save topic');
      } else {
        setError('Failed to save topic');
      }
    }
  };
  
  const handleDeleteTopic = async (topicId) => {
    if (!window.confirm('Are you sure you want to delete this topic?')) {
      return;
    }
    
    try {
      await api.delete(`/admin/topics/${topicId}`);
      setSuccess('Topic deleted successfully');
      loadTopics();
    } catch (error) {
      if (error.response) {
        setError(error.response.data.error || 'Failed to delete topic');
      } else {
        setError('Failed to delete topic');
      }
    }
  };
  
  const handleToggleAdminStatus = async (userId) => {
    try {
      await api.put(`/admin/users/${userId}/admin`);
      setSuccess('User admin status updated successfully');
      loadUsers();
    } catch (error) {
      if (error.response) {
        setError(error.response.data.error || 'Failed to update admin status');
      } else {
        setError('Failed to update admin status');
      }
    }
  };
  
  const handleGenerateQuestions = (topic) => {
    setSelectedTopic(topic);
    setGenerationForm({
      complexity: 'easy',
      count: 5,
      provider: 'ollama'
    });
    setGenerateDialogOpen(true);
  };

  const handleSubmitGeneration = async () => {
    if (!selectedTopic) return;
    
    setGenerating(true);
    
    // Create AbortController for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minutes timeout
    
    try {
      const response = await api.post('/admin/generate-questions', {
        topic_id: selectedTopic.id,
        complexity: generationForm.complexity,
        count: generationForm.count,
        provider: generationForm.provider
      }, {
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      setSuccess(`${response.data.message}. Generated ${response.data.questions_generated} questions, saved ${response.data.questions_saved} new ones.`);
      setGenerateDialogOpen(false);
      // Reload topics to update question counts
      loadTopics();
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        setError('Question generation timed out after 3 minutes. The server may still be processing your request.');
      } else if (error.response) {
        setError(error.response.data.error || 'Failed to generate questions');
      } else {
        setError('Failed to generate questions');
      }
    } finally {
      setGenerating(false);
    }
  };

  // Since we filter on the backend, we can use topics directly
  const filteredTopics = topics;
  
  if (loading) return <LoadingSpinner />;
  
  if (!user || !user.is_admin) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
        <AdminIcon sx={{ fontSize: 64, color: 'error.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          Access Denied
        </Typography>
        <Typography variant="body1" color="text.secondary">
          You need admin privileges to access this page.
        </Typography>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          <AdminIcon sx={{ mr: 2, verticalAlign: 'middle' }} />
          Admin Panel
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Manage topics, skills, and user permissions
        </Typography>
      </Box>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
          {error}
        </Alert>
      )}
      
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess('')}>
          {success}
        </Alert>
      )}
      
      {generating && (
        <Alert severity="info" sx={{ mb: 2 }} icon={<span>🤖</span>}>
          <strong>Generating questions for {selectedTopic?.topic}...</strong> 
          <br />
          Please wait while AI creates {generationForm.count} {generationForm.complexity} questions. 
          This process may take up to 3 minutes.
        </Alert>
      )}
      
      <Grid container spacing={4}>
        {/* Topics Management */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" component="h2">
                  <SchoolIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Topics & Skills
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={handleCreateTopic}
                >
                  Add Topic
                </Button>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <FormControl sx={{ minWidth: 200 }}>
                  <InputLabel>Filter by Grade</InputLabel>
                  <Select
                    value={selectedGrade}
                    label="Filter by Grade"
                    onChange={(e) => setSelectedGrade(e.target.value)}
                  >
                    <MenuItem value="">All Grades</MenuItem>
                    {[...Array(12)].map((_, i) => (
                      <MenuItem key={i + 1} value={i + 1}>
                        Grade {i + 1}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
              
              <TableContainer component={Paper} variant="outlined">
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Grade</TableCell>
                      <TableCell>Topic</TableCell>
                      <TableCell>Skill</TableCell>
                      <TableCell align="center">Questions Available</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {filteredTopics.map((topic) => (
                      <TableRow key={topic.id}>
                        <TableCell>
                          <Chip label={`Grade ${topic.grade_level}`} size="small" />
                        </TableCell>
                        <TableCell>
                          <Typography variant="subtitle2">
                            {topic.topic}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" color="text.secondary">
                            {topic.skill}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          {topic.question_counts ? (
                            <Box>
                              <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                                Total: {topic.question_counts.total}
                              </Typography>
                              <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center', alignItems: 'center' }}>
                                <Chip 
                                  label={`E: ${topic.question_counts.easy}`} 
                                  size="small" 
                                  color="success" 
                                  variant="outlined"
                                  sx={{ fontSize: '0.7rem', height: '20px', '& .MuiChip-label': { px: 1 } }}
                                />
                                <Chip 
                                  label={`M: ${topic.question_counts.medium}`} 
                                  size="small" 
                                  color="warning" 
                                  variant="outlined"
                                  sx={{ fontSize: '0.7rem', height: '20px', '& .MuiChip-label': { px: 1 } }}
                                />
                                <Chip 
                                  label={`H: ${topic.question_counts.hard}`} 
                                  size="small" 
                                  color="error" 
                                  variant="outlined"
                                  sx={{ fontSize: '0.7rem', height: '20px', '& .MuiChip-label': { px: 1 } }}
                                />
                              </Box>
                            </Box>
                          ) : (
                            <Typography variant="body2" color="text.secondary">
                              No data
                            </Typography>
                          )}
                        </TableCell>
                        <TableCell align="right">
                          <IconButton
                            size="small"
                            onClick={() => handleEditTopic(topic)}
                            color="primary"
                            disabled={generating}
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteTopic(topic.id)}
                            color="error"
                            disabled={generating}
                          >
                            <DeleteIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleGenerateQuestions(topic)}
                            color="secondary"
                            disabled={generating}
                            title={generating ? "Please wait, generation in progress..." : "Generate questions for this topic"}
                          >
                            <GenerateIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
        
        {/* User Management */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h5" component="h2" sx={{ mb: 3 }}>
                <PeopleIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                User Management
              </Typography>
              
              <TableContainer component={Paper} variant="outlined">
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>User</TableCell>
                      <TableCell>Admin</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {users.map((userItem) => (
                      <TableRow key={userItem.id}>
                        <TableCell>
                          <Typography variant="body2">
                            {userItem.first_name} {userItem.last_name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {userItem.email}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            variant={userItem.is_admin ? "contained" : "outlined"}
                            color={userItem.is_admin ? "success" : "primary"}
                            onClick={() => handleToggleAdminStatus(userItem.id)}
                            disabled={userItem.id === user.id}
                          >
                            {userItem.is_admin ? "Admin" : "User"}
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Topic Dialog */}
      <Dialog 
        open={topicDialogOpen} 
        onClose={() => setTopicDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {editingTopic ? 'Edit Topic' : 'Create New Topic'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="Topic Name"
              value={topicForm.topic}
              onChange={(e) => setTopicForm({ ...topicForm, topic: e.target.value })}
              sx={{ mb: 2 }}
            />
            
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Grade Level</InputLabel>
              <Select
                value={topicForm.grade_level}
                label="Grade Level"
                onChange={(e) => setTopicForm({ ...topicForm, grade_level: String(e.target.value) })}
              >
                {[...Array(12)].map((_, i) => (
                  <MenuItem key={i + 1} value={i + 1}>
                    Grade {i + 1}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              label="Skill Description"
              multiline
              rows={3}
              value={topicForm.skill}
              onChange={(e) => setTopicForm({ ...topicForm, skill: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTopicDialogOpen(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleSaveTopic}
            variant="contained"
            disabled={!topicForm.topic.trim() || !topicForm.skill.trim()}
          >
            {editingTopic ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Question Generation Dialog */}
      <Dialog
        open={generateDialogOpen}
        onClose={generating ? undefined : () => setGenerateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
        disableEscapeKeyDown={generating}
      >
        <DialogTitle>
          Generate Questions for Topic: {selectedTopic?.topic},  Skill: {selectedTopic?.skill} 
          , Grade: {selectedTopic?.grade_level}
          {generating && (
            <Typography variant="body2" color="primary" sx={{ fontStyle: 'italic', mt: 1 }}>
              🤖 AI is generating questions... This may take up to 3 minutes.
            </Typography>
          )}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Provider</InputLabel>
              <Select
                value={generationForm.provider}
                label="Provider"
                onChange={(e) => setGenerationForm({ ...generationForm, provider: e.target.value })}
                disabled={generating}
              >
                <MenuItem value="ollama">Ollama (Local)</MenuItem>
                <MenuItem value="openai">OpenAI (Cloud)</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Complexity</InputLabel>
              <Select
                value={generationForm.complexity}
                label="Complexity"
                onChange={(e) => setGenerationForm({ ...generationForm, complexity: e.target.value })}
                disabled={generating}
              >
                <MenuItem value="easy">Easy</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="hard">Hard</MenuItem>
              </Select>
            </FormControl>
            
            <TextField
              fullWidth
              label="Number of Questions"
              type="number"
              value={generationForm.count}
              onChange={(e) => setGenerationForm({ ...generationForm, count: parseInt(e.target.value) || 1 })}
              InputProps={{ inputProps: { min: 1, max: 20 } }}
              disabled={generating}
              helperText={generating ? "Please wait while questions are being generated..." : "Enter 1-20 questions"}
            />
            
            {generating && (
              <Box sx={{ mt: 3, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  ⏳ <strong>Processing Request</strong>
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  • AI is analyzing the topic: "{selectedTopic?.topic}"<br/>
                  • Generating {generationForm.count} {generationForm.complexity} questions<br/>
                  • Using {generationForm.provider} provider<br/>
                  • This process may take 1-3 minutes depending on complexity
                </Typography>
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setGenerateDialogOpen(false)}
            disabled={generating}
          >
            Cancel
          </Button>
          <Button 
            onClick={handleSubmitGeneration}
            variant="contained"
            disabled={generating || generationForm.count < 1 || generationForm.count > 20}
            startIcon={generating ? <span>🤖</span> : <span>✨</span>}
          >
            {generating ? 'Generating... Please Wait' : 'Generate Questions'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default AdminPanel;
