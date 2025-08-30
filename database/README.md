# Database Setup for Mathopedia

This directory contains the database schema and setup scripts for the Mathopedia application.

## Prerequisites

- MySQL 8.0 or higher
- MySQL client or MySQL Workbench

## Setup Instructions
    Install MySQL using Homebrew:
            brew install mysql
    Start the MySQL service:
            brew services start mysql
    Secure your MySQL installation (set root password, etc.):
            mysql_secure_installation. (root/root123)
    Log in to MySQL as root:
            mysql -u root -p
Create a new data
### 1. Create Database

```sql
CREATE DATABASE mathopedia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Create User (Optional but recommended)

```sql
CREATE USER 'mathopedia'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON mathopedia.* TO 'mathopedia'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Update Configuration

Update the database configuration in `backend/.env`:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=mathopedia
MYSQL_PASSWORD=your_secure_password
MYSQL_DB=mathopedia
```

### 4. Initialize Database

From the backend directory, run:

```bash
cd backend
python -m flask db init     # Initialize migrations (if using Flask-Migrate)
python -m flask init-db     # Create tables
python -m flask seed-db     # Seed sample data
```

### 5. Verify Setup

Log into MySQL and verify the tables were created:

```sql
USE mathopedia;
SHOW TABLES;
```

You should see:
- users
- questions
- user_answers
- daily_progress

## Database Schema

### Users Table
- id (Primary Key)
- first_name
- last_name
- email (Unique)
- password_hash
- created_at

### Questions Table
- id (Primary Key)
- grade_level (1-12)
- complexity (easy, medium, hard)
- topic
- question_text
- correct_answer
- explanation
- created_at

### User Answers Table
- id (Primary Key)
- user_id (Foreign Key)
- question_id (Foreign Key)
- user_answer
- is_correct
- answered_at

### Daily Progress Table
- id (Primary Key)
- user_id (Foreign Key)
- date
- questions_answered
- correct_answers
- total_time_spent

## Sample Queries

### Get user statistics
```sql
SELECT 
    u.first_name,
    COUNT(ua.id) as total_questions,
    SUM(ua.is_correct) as correct_answers,
    ROUND(SUM(ua.is_correct) / COUNT(ua.id) * 100, 2) as accuracy
FROM users u
LEFT JOIN user_answers ua ON u.id = ua.user_id
WHERE u.id = 1
GROUP BY u.id;
```

### Get daily progress
```sql
SELECT 
    date,
    questions_answered,
    correct_answers,
    ROUND(correct_answers / questions_answered * 100, 2) as accuracy
FROM daily_progress
WHERE user_id = 1
ORDER BY date DESC
LIMIT 30;
```
