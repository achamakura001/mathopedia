# Mathopedia API Documentation

## Overview

The Mathopedia API provides comprehensive functionality for a math learning platform. The API is built using Flask-RESTX and includes automatic Swagger/OpenAPI documentation.

## 🚀 Access Points

- **API Base URL (v1)**: `http://localhost:5000/api` (Original Flask routes)
- **API Base URL (v2)**: `http://localhost:5000/api/v2` (New Flask-RESTX with Swagger)
- **Swagger Documentation**: `http://localhost:5000/api/v2/docs/`
- **Health Check**: `http://localhost:5000/api/health`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## 📚 API Endpoints (Flask-RESTX v2)

### Authentication (`/api/v2/auth`)

#### `POST /api/v2/auth/login`
User login
- **Body**: `{"email": "user@example.com", "password": "password123"}`
- **Response**: JWT token and user information

#### `POST /api/auth/register`
User registration
- **Body**: `{"first_name": "John", "last_name": "Doe", "email": "john@example.com", "password": "password123"}`
- **Response**: JWT token and user information

#### `GET /api/auth/me`
Get current user information (requires authentication)

### Questions (`/api/questions`)

#### `GET /api/questions/`
Get questions with optional filtering
- **Query Parameters**:
  - `grade_level`: Filter by grade level
  - `complexity`: Filter by complexity (easy, medium, hard)
  - `topic`: Filter by topic
  - `limit`: Number of questions to return (default: 10)

#### `GET /api/questions/{id}`
Get a specific question by ID

#### `GET /api/questions/random`
Get a random question with optional filtering
- **Query Parameters**: Same as `/api/questions/`

#### `GET /api/questions/topics`
Get all topics with optional grade level filtering
- **Query Parameters**:
  - `grade_level`: Filter by grade level

#### `GET /api/questions/grades`
Get all available grade levels

### Answers (`/api/answers`)

#### `POST /api/answers/submit`
Submit an answer to a question
- **Body**: `{"question_id": 123, "user_answer": "42"}`
- **Response**: Correctness, correct answer, and explanation

#### `GET /api/answers/history`
Get user's answer history with pagination
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10, max: 100)
  - `grade_level`: Filter by grade level
  - `topic`: Filter by topic
  - `is_correct`: Filter by correctness (true/false)

#### `GET /api/answers/stats`
Get user's answer statistics

### Profile (`/api/profile`)

#### `GET /api/profile/`
Get comprehensive user profile with stats
- **Returns**: User info, overall stats, daily progress, grade-wise performance

#### `GET /api/profile/daily-progress`
Get daily progress for a date range
- **Query Parameters**:
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)

#### `GET /api/profile/achievements`
Get user achievements and milestones

#### `GET /api/profile/grade/{grade_level}/topics`
Get topic-wise performance breakdown for a specific grade
- **Example**: `/api/profile/grade/5/topics` for Grade 5 topics

### Admin (`/api/admin`)
*(Requires admin privileges)*

#### `GET /api/admin/users`
Get all users

#### `GET /api/admin/users/{id}`
Get detailed user information

#### `GET /api/admin/statistics`
Get platform statistics

#### `GET /api/admin/questions`
Get all questions with pagination
- **Query Parameters**:
  - `page`: Page number
  - `per_page`: Items per page
  - `grade_level`: Filter by grade level
  - `topic`: Filter by topic

#### `GET /api/admin/topics`
Get all topics

## 📊 Data Models

### User
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}
```

### Question
```json
{
  "id": 1,
  "grade_level": "5",
  "complexity": "medium",
  "topic": "Addition",
  "topic_id": 1,
  "question_text": "What is 2 + 2?",
  "correct_answer": "4",
  "explanation": "Adding 2 and 2 gives us 4.",
  "created_at": "2024-01-01T00:00:00"
}
```

### Grade Performance
```json
{
  "grade_level": "5",
  "grade_display": "Grade 5",
  "total_questions": 25,
  "correct_answers": 20,
  "accuracy": 80.0
}
```

### Topic Performance
```json
{
  "topic_id": 1,
  "topic_name": "Addition",
  "skill": "Basic addition skills",
  "total_questions": 10,
  "correct_answers": 8,
  "accuracy": 80.0
}
```

## 🔧 Features

### Grade-wise Performance
- **Automatic Grade Detection**: Uses distinct grade levels from topics table
- **Smart Formatting**: Numeric grades (1-12) prefixed with "Grade", others displayed as-is
- **Proper Joins**: Topics and questions joined by both `grade_level` and `topic` columns
- **Detailed Breakdown**: Click on any grade to see topic-wise performance

### Topic Performance Breakdown
- **Endpoint**: `GET /api/profile/grade/{grade_level}/topics`
- **Functionality**: Shows performance by topic for a selected grade
- **Sorting**: Topics sorted by accuracy and total questions attempted
- **Metadata**: Includes total topics and topics attempted counts

### Comprehensive Statistics
- Overall accuracy and progress tracking
- Daily progress with streak calculation
- Achievement system with multiple categories
- Admin analytics and user management

## 🛠️ Development

### Running the API
```bash
cd backend
python run.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Key Dependencies
- `Flask-RESTX`: API framework with Swagger documentation
- `Flask-JWT-Extended`: JWT authentication
- `Flask-SQLAlchemy`: Database ORM
- `Flask-CORS`: Cross-origin resource sharing

## 📖 Swagger Documentation

The API includes comprehensive Swagger documentation available at `/api/docs/`. This interactive documentation allows you to:

- Browse all available endpoints
- View request/response schemas
- Test API endpoints directly in the browser
- Authenticate and make authenticated requests
- Download OpenAPI specification

### Features of the Swagger UI:
- **Interactive Testing**: Try out API endpoints directly
- **Authentication Support**: Built-in JWT token management
- **Model Documentation**: Complete request/response schemas
- **Error Handling**: Detailed error response documentation

## 🔒 Security

- JWT-based authentication for all protected endpoints
- Admin-only endpoints for sensitive operations
- Input validation using Flask-RESTX
- CORS configuration for cross-origin requests

## 📈 Performance

- Efficient database queries with proper joins
- Pagination for large datasets
- Optimized grade and topic performance calculations
- Caching-friendly endpoint design

## 🚀 Getting Started

1. **Start the API**: `python run.py`
2. **Visit Swagger Docs**: Navigate to `http://localhost:5000/api/docs/`
3. **Register a User**: Use the `/api/auth/register` endpoint
4. **Login**: Use the `/api/auth/login` endpoint to get a JWT token
5. **Authenticate**: Click "Authorize" in Swagger UI and enter `Bearer <your_token>`
6. **Explore**: Try out the various endpoints!

## 📞 Support

For questions or issues with the API, please refer to the Swagger documentation at `/api/docs/` or check the application logs for detailed error information.
