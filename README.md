# Mathopedia - Interactive Math Learning Platform

A comprehensive, AI-powered math learning platform for students from 1st to 12th grade with adaptive questioning, progress tracking, and detailed explanations.

## ✨ Features

### 🎯 Core Learning Features
- **Grade-Specific Content**: Tailored math questions for grades 1-12
- **Adaptive Difficulty**: Easy, medium, and hard complexity levels
- **Smart Question Selection**: Never repeats answered questions
- **Detailed Explanations**: Step-by-step solutions for every question
- **Real-time Feedback**: Instant grading with educational insights

### 📊 Progress & Analytics
- **Daily Progress Tracking**: Monitor questions answered and accuracy
- **Performance Analytics**: Grade-wise performance visualization
- **Study Streaks**: Gamified learning with streak tracking
- **Achievement System**: Badges and milestones to motivate learning
- **Comprehensive Statistics**: Detailed performance insights

### 👤 User Experience
- **Secure Authentication**: Email-based registration and login
- **Beautiful UI**: Modern, responsive design with Material-UI
- **Personalized Dashboard**: Custom overview of learning progress
- **Profile Management**: Complete user profile with achievements

### 🤖 AI-Powered Question Generation
- **Multiple LLM Support**: Ollama (local), OpenAI GPT, and more
- **Dynamic Content**: AI-generated questions for unlimited practice
- **Topic Variety**: Covers all major math topics by grade level
- **Quality Assurance**: Structured prompts ensure high-quality questions

## 🏗️ Tech Stack

### Backend
- **Framework**: Python Flask with SQLAlchemy ORM
- **Database**: MySQL 8.0 with optimized schema
- **Authentication**: JWT tokens with refresh mechanism
- **API Design**: RESTful API with comprehensive error handling

### Frontend
- **Framework**: React 18 with functional components
- **UI Library**: Material-UI (MUI) with custom theming
- **State Management**: React Context API
- **Routing**: React Router v6
- **HTTP Client**: Axios with interceptors

### AI Integration
- **Local LLM**: Ollama with REST API
- **Cloud APIs**: OpenAI GPT, Anthropic Claude support
- **Question Generation**: Structured prompts for quality content
- **Flexibility**: Easy to swap between different AI providers

## 📁 Project Structure

```
Mathopedia/
├── backend/                    # Python Flask API Server
│   ├── app/
│   │   ├── models.py          # Database models (User, Question, etc.)
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   ├── questions.py   # Question management
│   │   │   ├── answers.py     # Answer submission & history
│   │   │   └── profile.py     # User profile & progress
│   │   └── services/          # Business logic
│   │       └── question_seeder.py # Sample data seeding
│   ├── config.py              # Configuration management
│   ├── run.py                 # Application entry point
│   └── requirements.txt       # Python dependencies
├── frontend/                   # React Web Application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── Navbar.js      # Navigation component
│   │   │   └── LoadingSpinner.js # Loading states
│   │   ├── pages/             # Main application pages
│   │   │   ├── Home.js        # Landing page
│   │   │   ├── Login.js       # Authentication
│   │   │   ├── Register.js    # User registration
│   │   │   ├── Dashboard.js   # User dashboard
│   │   │   ├── GradeSelection.js # Grade selection
│   │   │   ├── Quiz.js        # Interactive quiz interface
│   │   │   └── Profile.js     # User profile & stats
│   │   ├── contexts/          # React context providers
│   │   │   └── AuthContext.js # Authentication state
│   │   ├── services/          # API integration
│   │   │   ├── api.js         # Axios configuration
│   │   │   └── questionService.js # API methods
│   │   ├── App.js             # Main application component
│   │   └── index.js           # Application entry point
│   ├── package.json           # Node.js dependencies
│   └── public/                # Static assets
├── question-generator/         # AI Question Generator
│   ├── question_generator.py  # Main generator script
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Generator documentation
├── database/                   # Database setup & docs
│   └── README.md              # Database schema & setup
├── setup.sh                   # Development setup script
├── start-dev.sh              # Development startup script
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Automated Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Mathopedia

# Run the automated setup script
./setup.sh

# Start all services
./start-dev.sh
```

### 2. Manual Setup

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python run.py init-db
python run.py seed-db
python run.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

#### Database Setup
```sql
CREATE DATABASE mathopedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mathopedia'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON mathopedia.* TO 'mathopedia'@'localhost';
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/ (if implemented)

## 📚 Detailed Documentation

- [Backend Setup Guide](backend/README.md)
- [Frontend Setup Guide](frontend/README.md)
- [Database Schema](database/README.md)
- [Question Generator](question-generator/README.md)

## 🎯 Key Features Explained

### Adaptive Question System
The platform intelligently selects questions based on:
- User's grade level
- Previously answered questions (no repeats)
- Complexity distribution (mix of easy, medium, hard)
- Topic coverage across different math areas

### Progress Tracking
Comprehensive tracking includes:
- Daily question counts and accuracy
- Study streaks and consistency
- Grade-wise performance analysis
- Historical progress visualization

### AI Question Generation
Flexible AI integration supporting:
- **Ollama**: Local LLM for privacy and cost-effectiveness
- **OpenAI GPT**: Cloud-based for higher quality
- **Custom Prompts**: Structured prompts ensure educational quality
- **Batch Generation**: Efficient bulk question creation

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=mathopedia
MYSQL_PASSWORD=your-password
MYSQL_DB=mathopedia

# JWT
JWT_SECRET_KEY=your-jwt-secret

# LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OPENAI_API_KEY=your-openai-key  # Optional
```

#### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📖 API Reference

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Current user info

### Questions & Quizzes
- `GET /api/questions/grade/{grade}` - Get questions for grade
- `GET /api/questions/{id}` - Get specific question
- `GET /api/questions/stats/grade/{grade}` - Grade statistics

### Answer Management
- `POST /api/answers/submit` - Submit answer
- `GET /api/answers/history` - Answer history
- `GET /api/answers/stats` - Answer statistics

### User Profile
- `GET /api/profile/` - User profile & stats
- `GET /api/profile/daily-progress` - Daily progress
- `GET /api/profile/achievements` - User achievements

## 🎨 UI/UX Features

### Modern Design
- Material-UI components with custom theming
- Responsive design for all devices
- Smooth animations and transitions
- Intuitive navigation and user flow

### Accessibility
- Keyboard navigation support
- Screen reader friendly
- High contrast mode support
- Clear visual hierarchy

## 🔐 Security Features

- JWT-based authentication with refresh tokens
- Password hashing with bcrypt
- SQL injection prevention with parameterized queries
- CORS configuration for API security
- Input validation and sanitization

## 📊 Performance Optimization

### Backend
- Database query optimization
- Connection pooling
- Efficient data serialization
- Caching strategies for frequently accessed data

### Frontend
- Code splitting and lazy loading
- Optimized bundle size
- Image optimization
- Progressive loading for better UX

## 🧪 Testing & Quality

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Code Quality
- ESLint for JavaScript code quality
- Prettier for code formatting
- Python PEP 8 compliance
- Git hooks for pre-commit checks

## 🚀 Production Deployment

⚠️ **Having deployment issues?** Check our comprehensive [Deployment Guide](DEPLOYMENT_GUIDE.md) for fixing common API configuration problems.

### Backend Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Using Docker
docker build -t mathopedia-backend .
docker run -p 5000:5000 mathopedia-backend
```

### Frontend Deployment

**🆕 Auto-Detection (No Configuration Needed):**
```bash
cd frontend
# Remove any old .env file
rm .env 2>/dev/null || true
npm start
# App automatically detects your host and configures API calls
```

**Quick Setup:**
```bash
cd frontend
./setup-env.sh  # Interactive environment setup
npm run build
```

**Manual Setup:**
```bash
# Build for production
npm run build

# Configure API URL for your deployment
echo "REACT_APP_API_URL=http://your-server:5000" > .env

# Serve static files
npm install -g serve
serve -s build

# Or deploy to Netlify/Vercel
```

### Common Deployment Issues

- **API calls go to localhost**: See [API Configuration Guide](frontend/API_CONFIGURATION.md)
- **CORS errors**: Update backend CORS settings for your domain
- **404 on refresh**: Configure your web server for SPA routing

### Database Production Setup
- Use connection pooling
- Set up read replicas for scaling
- Configure automated backups
- Implement proper indexing strategy

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push and create PR
git push origin feature/new-feature
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support & Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify MySQL is running
   - Check credentials in .env file
   - Ensure database exists

2. **Frontend API Errors**
   - Verify backend is running on port 5000
   - Check CORS configuration
   - Verify API endpoints

3. **Ollama Connection Issues**
   - Start Ollama service: `ollama serve`
   - Pull required model: `ollama pull llama2`
   - Check Ollama URL in configuration

### Getting Help
- Check the detailed README files in each directory
- Review the troubleshooting sections
- Create an issue on GitHub
- Check the logs for error messages

## 🌟 Future Enhancements

### Planned Features
- [ ] Mobile app (React Native)
- [ ] Multiplayer quiz mode
- [ ] Teacher dashboard
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Video explanations
- [ ] Voice input support

### AI Improvements
- [ ] More sophisticated question generation
- [ ] Adaptive difficulty adjustment
- [ ] Personalized learning paths
- [ ] Natural language question answering

## 📈 Performance Metrics

### Current Capabilities
- **Concurrent Users**: 100+ (with proper scaling)
- **Question Generation**: 10-50 questions per minute
- **Database**: Supports millions of questions and answers
- **Response Time**: < 200ms for most API calls

## 🎯 Learning Outcomes

Students using Mathopedia will:
- Improve mathematical problem-solving skills
- Develop consistent study habits
- Gain confidence through immediate feedback
- Track their progress over time
- Prepare effectively for grade-level assessments

---

**Built with ❤️ for better math education**

For detailed setup instructions, please refer to the individual README files in each directory.
