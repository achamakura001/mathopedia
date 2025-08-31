from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict


# User Schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    created_at: datetime


class GenerateQuestions(BaseModel):
    topic_id: int
    complexity: str
    count: int = 5
    provider: str = "ollama"


# Question Schemas
class QuestionCreate(BaseModel):
    grade_level: str
    complexity: str
    topic: str
    topic_id: Optional[int] = None
    question_text: str
    correct_answer: str
    explanation: str


class QuestionUpdate(BaseModel):
    grade_level: Optional[str] = None
    complexity: Optional[str] = None
    topic: Optional[str] = None
    topic_id: Optional[int] = None
    question_text: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class TopicReference(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    topic: str
    skill: str
    grade_level: str


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    grade_level: str
    complexity: str
    topic: str
    topic_id: Optional[int] = None
    topic_ref: Optional[TopicReference] = None
    question_text: str
    correct_answer: str
    explanation: str
    created_at: datetime


# Answer Schemas
class AnswerSubmit(BaseModel):
    question_id: int
    user_answer: str


class UserAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    answered_at: datetime
    question: Optional[QuestionResponse] = None


# Progress Schemas
class DailyProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    date: date
    questions_answered: int
    correct_answers: int
    accuracy: float
    total_time_spent: int


# Topic Schemas
class TopicCreate(BaseModel):
    topic: str
    skill: str
    grade_level: str


class TopicUpdate(BaseModel):
    topic: Optional[str] = None
    skill: Optional[str] = None
    grade_level: Optional[str] = None


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    topic: str
    skill: str
    grade_level: str
    created_at: datetime
    updated_at: datetime


# Quiz Schemas
class QuizFilter(BaseModel):
    grade_level: Optional[str] = None
    topic: Optional[str] = None
    complexity: Optional[str] = None
    count: int = 10


# Auth Response Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None


# Standard Response Schemas
class Message(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str


# Analytics Schemas
class ProgressStats(BaseModel):
    total_questions: int
    correct_answers: int
    accuracy: float
    total_time: int
    weekly_progress: List[DailyProgressResponse]


class TopicStats(BaseModel):
    topic: str
    questions_answered: int
    correct_answers: int
    accuracy: float


class UserStats(BaseModel):
    user: UserResponse
    progress_stats: ProgressStats
    topic_stats: List[TopicStats]
