from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from app import db
from app.models import Question, Topic
from app.utils import get_current_user_id
from app.api.models import question_model, question_request_model, topic_model, error_model

api = Namespace('questions', description='Question management operations')

@api.route('/')
class QuestionListResource(Resource):
    @api.doc('get_questions')
    @api.param('grade_level', 'Filter by grade level', type='string')
    @api.param('complexity', 'Filter by complexity', type='string', enum=['easy', 'medium', 'hard'])
    @api.param('topic', 'Filter by topic', type='string')
    @api.param('limit', 'Number of questions to return', type='integer', default=10)
    @api.marshal_list_with(question_model)
    @api.response(200, 'Success', [question_model])
    @api.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get questions with optional filtering"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        # Get query parameters
        grade_level = request.args.get('grade_level')
        complexity = request.args.get('complexity')
        topic = request.args.get('topic')
        limit = request.args.get('limit', 10, type=int)
        
        # Build query
        query = Question.query
        
        if grade_level:
            query = query.filter(Question.grade_level == grade_level)
        
        if complexity:
            query = query.filter(Question.complexity == complexity)
        
        if topic:
            query = query.filter(Question.topic == topic)
        
        # Get random questions
        questions = query.order_by(func.random()).limit(limit).all()
        
        return [question.to_dict() for question in questions]

@api.route('/<int:question_id>')
class QuestionResource(Resource):
    @api.doc('get_question')
    @api.marshal_with(question_model)
    @api.response(200, 'Success', question_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(404, 'Question not found', error_model)
    @jwt_required()
    def get(self, question_id):
        """Get a specific question by ID"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        question = Question.query.get(question_id)
        if not question:
            api.abort(404, 'Question not found')
        
        return question.to_dict()

@api.route('/random')
class RandomQuestionResource(Resource):
    @api.doc('get_random_question')
    @api.param('grade_level', 'Filter by grade level', type='string')
    @api.param('complexity', 'Filter by complexity', type='string', enum=['easy', 'medium', 'hard'])
    @api.param('topic', 'Filter by topic', type='string')
    @api.marshal_with(question_model)
    @api.response(200, 'Success', question_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(404, 'No questions found', error_model)
    @jwt_required()
    def get(self):
        """Get a random question with optional filtering"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        # Get query parameters
        grade_level = request.args.get('grade_level')
        complexity = request.args.get('complexity')
        topic = request.args.get('topic')
        
        # Build query
        query = Question.query
        
        if grade_level:
            query = query.filter(Question.grade_level == grade_level)
        
        if complexity:
            query = query.filter(Question.complexity == complexity)
        
        if topic:
            query = query.filter(Question.topic == topic)
        
        # Get random question
        question = query.order_by(func.random()).first()
        
        if not question:
            api.abort(404, 'No questions found matching the criteria')
        
        return question.to_dict()

@api.route('/topics')
class TopicListResource(Resource):
    @api.doc('get_topics')
    @api.param('grade_level', 'Filter by grade level', type='string')
    @api.marshal_list_with(topic_model)
    @api.response(200, 'Success', [topic_model])
    @api.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get all topics with optional grade level filtering"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        grade_level = request.args.get('grade_level')
        
        query = Topic.query
        
        if grade_level:
            query = query.filter(Topic.grade_level == grade_level)
        
        topics = query.order_by(Topic.grade_level, Topic.topic).all()
        
        return [topic.to_dict() for topic in topics]

@api.route('/grades')
class GradeLevelsResource(Resource):
    @api.doc('get_grade_levels')
    @api.marshal_with(fields.Raw)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized', error_model)
    @jwt_required()
    def get(self):
        """Get all available grade levels"""
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            api.abort(401, 'Invalid user authentication')
        
        # Get distinct grade levels from topics
        grade_levels = db.session.query(Topic.grade_level.distinct()).order_by(Topic.grade_level).all()
        
        # Format grade levels with display names
        formatted_grades = []
        for (grade_level,) in grade_levels:
            if grade_level.isdigit():
                grade_display = f"Grade {grade_level}"
            else:
                grade_display = grade_level
            
            formatted_grades.append({
                'grade_level': grade_level,
                'grade_display': grade_display
            })
        
        return {
            'grade_levels': formatted_grades
        }
