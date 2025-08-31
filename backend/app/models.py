from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, Date, 
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import Base

# Password hashing
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = relationship('UserAnswer', back_populates='user', cascade='all, delete-orphan')
    progress = relationship('DailyProgress', back_populates='user', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat()
        }


class Question(Base):
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    grade_level = Column(String(50), nullable=False)  # 1-12 or "Competitive Exams"
    complexity = Column(String(20), nullable=False)  # easy, medium, hard
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=True)  # Reference to Topic
    topic = Column(String(100), nullable=False)  # Keep for backward compatibility
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_answers = relationship('UserAnswer', back_populates='question')
    topic_ref = relationship('Topic', back_populates='questions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'grade_level': self.grade_level,
            'complexity': self.complexity,
            'topic': self.topic,
            'topic_id': self.topic_id,
            'topic_ref': self.topic_ref.to_dict() if self.topic_ref else None,
            'question_text': self.question_text,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'created_at': self.created_at.isoformat()
        }


class UserAnswer(Base):
    __tablename__ = 'user_answers'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    user_answer = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='answers')
    question = relationship('Question', back_populates='user_answers')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'answered_at': self.answered_at.isoformat(),
            'question': self.question.to_dict() if self.question else None
        }


class DailyProgress(Base):
    __tablename__ = 'daily_progress'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    questions_answered = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # in minutes
    
    # Composite unique constraint
    __table_args__ = (UniqueConstraint('user_id', 'date', name='unique_user_date'),)
    
    # Relationships
    user = relationship('User', back_populates='progress')
    
    def to_dict(self):
        accuracy = 0
        if self.questions_answered > 0:
            accuracy = round(self.correct_answers / self.questions_answered * 100, 2)
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'questions_answered': self.questions_answered,
            'correct_answers': self.correct_answers,
            'accuracy': accuracy,
            'total_time_spent': self.total_time_spent
        }


class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100), nullable=False)
    skill = Column(Text, nullable=False)
    grade_level = Column(String(50), nullable=False)  # Support "Competitive Exams"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint for topic name and grade level
    __table_args__ = (UniqueConstraint('topic', 'grade_level', name='unique_topic_grade'),)
    
    # Relationships
    questions = relationship('Question', back_populates='topic_ref')
    
    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'skill': self.skill,
            'grade_level': self.grade_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
