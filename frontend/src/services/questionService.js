import api from './api';

export const questionService = {
  // Get questions for a specific grade
  getQuestionsForGrade: async (gradeLevel) => {
    const response = await api.get(`/api/questions/grade/${gradeLevel}`);
    return response.data;
  },

  // Get questions for competitive exams
  getCompetitiveQuestions: async () => {
    const response = await api.get(`/api/questions/grade/competitive`);
    return response.data;
  },

  // Get a specific question
  getQuestion: async (questionId) => {
    const response = await api.get(`/api/questions/${questionId}`);
    return response.data;
  },

  // Get grade statistics
  getGradeStats: async (gradeLevel) => {
    const response = await api.get(`/api/questions/stats/grade/${gradeLevel}`);
    return response.data;
  },

  // Get competitive exam statistics
  getCompetitiveStats: async () => {
    const response = await api.get(`/api/questions/stats/grade/competitive`);
    return response.data;
  },
};

export const answerService = {
  // Submit answer
  submitAnswer: async (questionId, userAnswer) => {
    const response = await api.post('/api/answers/submit', {
      question_id: questionId,
      user_answer: userAnswer,
    });
    return response.data;
  },

  // Get answer history
  getAnswerHistory: async (page = 1, perPage = 20, gradeLevel = null) => {
    const params = { page, per_page: perPage };
    if (gradeLevel) {
      params.grade_level = gradeLevel;
    }
    
    const response = await api.get('/api/answers/history', { params });
    return response.data;
  },

  // Get answer statistics
  getAnswerStats: async () => {
    const response = await api.get('/api/answers/stats');
    return response.data;
  },
};

export const profileService = {
  // Get user profile
  getProfile: async () => {
    const response = await api.get('/api/profile/');
    return response.data;
  },

  // Get daily progress
  getDailyProgress: async (startDate = null, endDate = null) => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await api.get('/api/profile/daily-progress', { params });
    return response.data;
  },

  // Get achievements
  getAchievements: async () => {
    const response = await api.get('/api/profile/achievements');
    return response.data;
  },
};
