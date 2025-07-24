from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('UserAnswer', backref='user', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('DailyProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    
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

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    grade_level = db.Column(db.String(50), nullable=False)  # 1-12 or "Competitive Exams"
    complexity = db.Column(db.String(20), nullable=False)  # easy, medium, hard
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)  # Reference to Topic
    topic = db.Column(db.String(100), nullable=False)  # Keep for backward compatibility
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_answers = db.relationship('UserAnswer', backref='question', lazy=True)
    
    def get_or_create_topic_reference(self):
        """Get or create a topic reference based on grade_level and topic name"""
        if not self.topic_id:
            topic = Topic.query.filter_by(topic=self.topic, grade_level=self.grade_level).first()
            if topic:
                self.topic_id = topic.id
                db.session.commit()
        return self.topic_id
    
    def to_dict(self):
        # Ensure topic_id is set if possible
        self.get_or_create_topic_reference()
        
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

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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

class DailyProgress(db.Model):
    __tablename__ = 'daily_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    questions_answered = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    total_time_spent = db.Column(db.Integer, default=0)  # in minutes
    
    # Composite unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'date', name='unique_user_date'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'questions_answered': self.questions_answered,
            'correct_answers': self.correct_answers,
            'accuracy': round(self.correct_answers / self.questions_answered * 100, 2) if self.questions_answered > 0 else 0,
            'total_time_spent': self.total_time_spent
        }

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.Text, nullable=False)
    grade_level = db.Column(db.String(50), nullable=False)  # Changed from Integer to String to support "Competitive Exams"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint for topic name and grade level
    __table_args__ = (db.UniqueConstraint('topic', 'grade_level', name='unique_topic_grade'),)
    
    # Relationships
    questions = db.relationship('Question', backref='topic_ref', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'skill': self.skill,
            'grade_level': self.grade_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
