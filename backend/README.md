# Backend Setup Guide

## Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-this-in-production
   
   # Database Configuration
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your-mysql-username
   MYSQL_PASSWORD=your-mysql-password
   MYSQL_DB=mathopedia
   
   # JWT Configuration
   JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production
   
   # LLM Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

5. **Initialize the database:**
   ```bash
   python run.py init-db
   python run.py seed-db
   ```

## Running the Application

1. **Start the development server:**
   ```bash
   python run.py
   ```
   
   The API will be available at `http://localhost:5000`

2. **Test the API:**
   ```bash
   curl http://localhost:5000/api/auth/register -X POST \
     -H "Content-Type: application/json" \
     -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"password123"}'
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user

### Questions
- `GET /api/questions/grade/{grade}` - Get questions for grade
- `GET /api/questions/{id}` - Get specific question
- `GET /api/questions/stats/grade/{grade}` - Get grade statistics

### Answers
- `POST /api/answers/submit` - Submit answer
- `GET /api/answers/history` - Get answer history
- `GET /api/answers/stats` - Get answer statistics

### Profile
- `GET /api/profile/` - Get user profile
- `GET /api/profile/daily-progress` - Get daily progress
- `GET /api/profile/achievements` - Get user achievements

## Development

### Adding New Questions
Use the question generator utility:
```bash
cd ../question-generator
python question_generator.py --grade 5 --topic "Fractions" --complexity "medium" --count 10 --save
```

### Database Migrations
If you modify the database models:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Testing
Run the development server and test endpoints using a tool like Postman or curl.

## Production Deployment

1. **Set environment variables:**
   ```env
   FLASK_ENV=production
   SECRET_KEY=strong-random-secret-key
   JWT_SECRET_KEY=strong-random-jwt-key
   ```

2. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **Set up reverse proxy (nginx recommended)**
4. **Use a production database with proper credentials**
5. **Enable HTTPS**
