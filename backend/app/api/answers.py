from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from sqlalchemy import func

from app import db
from app.models import UserAnswer, Question, DailyProgress
from app.utils import get_current_user_id
from app.api.models import (
    submit_answer_model, 
    answer_response_model, 
    user_answer_model, 
    error_model
)

api = Namespace('answers', description='Answer submission and history operations')

@api.route('/submit')
class SubmitAnswerResource(Resource):
    @api.doc('submit_answer')
    @api.expect(submit_answer_model, validate=True)
    @api.marshal_with(answer_response_model)
    @api.response(200, 'Answer submitted successfully', answer_response_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(404, 'Question not found', error_model)
    @api.response(400, 'Validation error', error_model)
    @jwt_required()
    def post(self):
        """Submit an answer to a question"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        data = api.payload
        question_id = data['question_id']
        user_answer = data['user_answer']
        
        # Get the question
        question = Question.query.get(question_id)
        if not question:
            api.abort(404, 'Question not found')
        
        # Check if answer is correct
        is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
        
        # Save user answer
        answer_record = UserAnswer(
            user_id=current_user_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct
        )
        
        try:
            db.session.add(answer_record)
            
            # Update daily progress
            today = date.today()
            daily_progress = DailyProgress.query.filter_by(
                user_id=current_user_id,
                date=today
            ).first()
            
            if not daily_progress:
                daily_progress = DailyProgress(
                    user_id=current_user_id,
                    date=today,
                    questions_answered=1,
                    correct_answers=1 if is_correct else 0
                )
                db.session.add(daily_progress)
            else:
                daily_progress.questions_answered += 1
                if is_correct:
                    daily_progress.correct_answers += 1
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            api.abort(400, f'Failed to submit answer: {str(e)}')
        
        return {
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'user_answer': user_answer
        }

@api.route('/history')
class AnswerHistoryResource(Resource):
    @api.doc('get_answer_history')
    @api.param('page', 'Page number', type='integer', default=1)
    @api.param('per_page', 'Items per page', type='integer', default=10)
    @api.param('grade_level', 'Filter by grade level', type='string')
    @api.param('topic', 'Filter by topic', type='string')
    @api.param('is_correct', 'Filter by correctness', type='boolean')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get user's answer history with pagination and filtering"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)  # Max 100 per page
        grade_level = request.args.get('grade_level')
        topic = request.args.get('topic')
        is_correct = request.args.get('is_correct', type=bool)
        
        # Build query
        query = UserAnswer.query.filter_by(user_id=current_user_id).join(Question)
        
        if grade_level:
            query = query.filter(Question.grade_level == grade_level)
        
        if topic:
            query = query.filter(Question.topic == topic)
        
        if is_correct is not None:
            query = query.filter(UserAnswer.is_correct == is_correct)
        
        # Order by most recent first
        query = query.order_by(UserAnswer.answered_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'answers': [answer.to_dict() for answer in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }

@api.route('/stats')
class AnswerStatsResource(Resource):
    @api.doc('get_answer_stats')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get user's answer statistics"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        # Total stats
        total_answers = UserAnswer.query.filter_by(user_id=current_user_id).count()
        correct_answers = UserAnswer.query.filter_by(
            user_id=current_user_id,
            is_correct=True
        ).count()
        
        overall_accuracy = round(correct_answers / total_answers * 100, 2) if total_answers > 0 else 0
        
        # Stats by grade level
        grade_stats = db.session.query(
            Question.grade_level,
            func.count(UserAnswer.id).label('total'),
            func.sum(func.cast(UserAnswer.is_correct, db.Integer)).label('correct')
        ).join(Question).filter(
            UserAnswer.user_id == current_user_id
        ).group_by(Question.grade_level).all()
        
        grade_performance = []
        for grade_level, total, correct in grade_stats:
            accuracy = round((correct / total) * 100, 2) if total > 0 else 0
            grade_display = f"Grade {grade_level}" if grade_level.isdigit() else grade_level
            
            grade_performance.append({
                'grade_level': grade_level,
                'grade_display': grade_display,
                'total_questions': total,
                'correct_answers': correct,
                'accuracy': accuracy
            })
        
        # Stats by topic
        topic_stats = db.session.query(
            Question.topic,
            Question.grade_level,
            func.count(UserAnswer.id).label('total'),
            func.sum(func.cast(UserAnswer.is_correct, db.Integer)).label('correct')
        ).join(Question).filter(
            UserAnswer.user_id == current_user_id
        ).group_by(Question.topic, Question.grade_level).all()
        
        topic_performance = []
        for topic, grade_level, total, correct in topic_stats:
            accuracy = round((correct / total) * 100, 2) if total > 0 else 0
            
            topic_performance.append({
                'topic': topic,
                'grade_level': grade_level,
                'total_questions': total,
                'correct_answers': correct,
                'accuracy': accuracy
            })
        
        return {
            'overall': {
                'total_questions': total_answers,
                'correct_answers': correct_answers,
                'overall_accuracy': overall_accuracy
            },
            'by_grade': grade_performance,
            'by_topic': topic_performance
        }
