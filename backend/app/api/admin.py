from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from app import db
from app.models import User, Question, Topic, UserAnswer, DailyProgress
from app.utils import get_current_user_id
from app.api.models import (
    user_model, 
    question_model, 
    topic_model, 
    error_model
)

api = Namespace('admin', description='Admin operations (requires admin privileges)')

def require_admin():
    """Helper function to check if current user is admin"""
    current_user_id = get_current_user_id()
    if not current_user_id:
        api.abort(401, 'Invalid user authentication')
    
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        api.abort(403, 'Admin privileges required')
    
    return user

@api.route('/users')
class AdminUsersResource(Resource):
    @api.doc('get_all_users')
    @api.marshal_list_with(user_model)
    @api.response(200, 'Success', [user_model])
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Admin privileges required', error_model)
    @jwt_required()
    def get(self):
        """Get all users (admin only)"""
        require_admin()
        
        users = User.query.order_by(User.created_at.desc()).all()
        return [user.to_dict() for user in users]

@api.route('/users/<int:user_id>')
class AdminUserResource(Resource):
    @api.doc('get_user_details')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Admin privileges required', error_model)
    @api.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self, user_id):
        """Get detailed user information (admin only)"""
        require_admin()
        
        user = User.query.get(user_id)
        if not user:
            api.abort(404, 'User not found')
        
        # Get user statistics
        total_answers = UserAnswer.query.filter_by(user_id=user_id).count()
        correct_answers = UserAnswer.query.filter_by(
            user_id=user_id,
            is_correct=True
        ).count()
        
        # Get daily progress
        daily_progress = DailyProgress.query.filter_by(user_id=user_id).all()
        study_days = len([p for p in daily_progress if p.questions_answered > 0])
        
        user_data = user.to_dict()
        user_data.update({
            'statistics': {
                'total_questions_answered': total_answers,
                'correct_answers': correct_answers,
                'overall_accuracy': round(correct_answers / total_answers * 100, 2) if total_answers > 0 else 0,
                'total_study_days': study_days
            },
            'recent_activity': [p.to_dict() for p in daily_progress[-7:]]  # Last 7 days
        })
        
        return user_data

@api.route('/statistics')
class AdminStatisticsResource(Resource):
    @api.doc('get_admin_statistics')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Admin privileges required', error_model)
    @jwt_required()
    def get(self):
        """Get platform statistics (admin only)"""
        require_admin()
        
        # User statistics
        total_users = User.query.count()
        admin_users = User.query.filter_by(is_admin=True).count()
        active_users = User.query.join(UserAnswer).distinct().count()
        
        # Question statistics
        total_questions = Question.query.count()
        questions_by_grade = db.session.query(
            Question.grade_level,
            func.count(Question.id)
        ).group_by(Question.grade_level).all()
        
        # Answer statistics
        total_answers = UserAnswer.query.count()
        correct_answers = UserAnswer.query.filter_by(is_correct=True).count()
        
        # Topic statistics
        total_topics = Topic.query.count()
        topics_by_grade = db.session.query(
            Topic.grade_level,
            func.count(Topic.id)
        ).group_by(Topic.grade_level).all()
        
        return {
            'users': {
                'total': total_users,
                'admins': admin_users,
                'active': active_users
            },
            'questions': {
                'total': total_questions,
                'by_grade': [{'grade': grade, 'count': count} for grade, count in questions_by_grade]
            },
            'answers': {
                'total': total_answers,
                'correct': correct_answers,
                'accuracy': round(correct_answers / total_answers * 100, 2) if total_answers > 0 else 0
            },
            'topics': {
                'total': total_topics,
                'by_grade': [{'grade': grade, 'count': count} for grade, count in topics_by_grade]
            }
        }

@api.route('/questions')
class AdminQuestionsResource(Resource):
    @api.doc('get_all_questions')
    @api.param('page', 'Page number', type='integer', default=1)
    @api.param('per_page', 'Items per page', type='integer', default=20)
    @api.param('grade_level', 'Filter by grade level', type='string')
    @api.param('topic', 'Filter by topic', type='string')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Admin privileges required', error_model)
    @jwt_required()
    def get(self):
        """Get all questions with pagination (admin only)"""
        require_admin()
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        grade_level = request.args.get('grade_level')
        topic = request.args.get('topic')
        
        query = Question.query
        
        if grade_level:
            query = query.filter(Question.grade_level == grade_level)
        
        if topic:
            query = query.filter(Question.topic == topic)
        
        pagination = query.order_by(Question.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'questions': [q.to_dict() for q in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }

@api.route('/topics')
class AdminTopicsResource(Resource):
    @api.doc('get_all_topics')
    @api.marshal_list_with(topic_model)
    @api.response(200, 'Success', [topic_model])
    @api.response(401, 'Unauthorized', error_model)
    @api.response(403, 'Admin privileges required', error_model)
    @jwt_required()
    def get(self):
        """Get all topics (admin only)"""
        require_admin()
        
        topics = Topic.query.order_by(Topic.grade_level, Topic.topic).all()
        return [topic.to_dict() for topic in topics]
