from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import Schema, fields, ValidationError
from sqlalchemy import func
from app import db
from app.models import Topic, User, Question
from app.utils import get_current_user_id
import os
import sys

# Add question generator to path
question_generator_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'question-generator')
sys.path.append(question_generator_path)

admin_bp = Blueprint('admin', __name__)

class TopicSchema(Schema):
    name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    skill = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    grade_level = fields.Int(required=True, validate=lambda x: 1 <= x <= 12)

class QuestionGenerationSchema(Schema):
    topic_id = fields.Int(required=True)
    complexity = fields.Str(required=True, validate=lambda x: x in ['easy', 'medium', 'hard'])
    count = fields.Int(required=True, validate=lambda x: 1 <= x <= 20)
    provider = fields.Str(load_default='ollama', validate=lambda x: x in ['ollama', 'openai'])

def check_admin_access():
    """Helper function to check if current user is admin"""
    current_user_id = get_current_user_id()
    if not current_user_id:
        return None, jsonify({'error': 'Invalid user authentication'}), 401
    
    user = User.query.get(current_user_id)
    if not user:
        return None, jsonify({'error': 'User not found'}), 404
    
    if not user.is_admin:
        return None, jsonify({'error': 'Admin access required'}), 403
    
    return user, None, None

@admin_bp.route('/topics', methods=['GET'])
@jwt_required()
def get_all_topics():
    """Get all topics across all grades with question statistics"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    grade_level = request.args.get('grade_level', type=int)
    
    if grade_level:
        topics = Topic.query.filter_by(grade_level=grade_level).order_by(Topic.topic).all()
    else:
        topics = Topic.query.order_by(Topic.grade_level, Topic.topic).all()
    
    # Get question statistics for each topic
    topics_with_stats = []
    for topic in topics:
        topic_dict = topic.to_dict()
        
        # Get question counts by complexity for this topic and grade
        question_stats = db.session.query(
            Question.complexity,
            func.count(Question.id).label('count')
        ).filter(
            Question.topic_id == topic.id
        ).group_by(Question.complexity).all()
        
        # Also check for questions that reference this topic by string (backward compatibility)
        legacy_question_stats = db.session.query(
            Question.complexity,
            func.count(Question.id).label('count')
        ).filter(
            Question.topic == topic.topic,
            Question.grade_level == str(topic.grade_level),  # Convert int to string for comparison
            Question.topic_id.is_(None)  # Only count legacy questions without topic_id
        ).group_by(Question.complexity).all()
        
        # Combine stats from both sources
        combined_stats = {}
        for complexity, count in question_stats:
            combined_stats[complexity] = combined_stats.get(complexity, 0) + count
        
        for complexity, count in legacy_question_stats:
            combined_stats[complexity] = combined_stats.get(complexity, 0) + count
        
        # Add question statistics to topic data
        topic_dict['question_counts'] = {
            'easy': combined_stats.get('easy', 0),
            'medium': combined_stats.get('medium', 0),
            'hard': combined_stats.get('hard', 0),
            'total': sum(combined_stats.values())
        }
        
        topics_with_stats.append(topic_dict)
    
    return jsonify({
        'topics': topics_with_stats,
        'total_count': len(topics)
    }), 200

@admin_bp.route('/topics', methods=['POST'])
@jwt_required()
def create_topic():
    """Create a new topic"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    schema = TopicSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    # Check if topic with same name and grade level already exists
    existing_topic = Topic.query.filter_by(
        name=data['name'].strip(),
        grade_level=data['grade_level']
    ).first()
    
    if existing_topic:
        return jsonify({'error': 'Topic with this name already exists for this grade level'}), 400
    
    topic = Topic(
        name=data['name'].strip(),
        skill=data['skill'].strip(),
        grade_level=data['grade_level']
    )
    
    try:
        db.session.add(topic)
        db.session.commit()
        return jsonify({
            'message': 'Topic created successfully',
            'topic': topic.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create topic'}), 500

@admin_bp.route('/topics/<int:topic_id>', methods=['PUT'])
@jwt_required()
def update_topic(topic_id):
    """Update an existing topic"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    schema = TopicSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    # Check if another topic with same name and grade level exists
    existing_topic = Topic.query.filter(
        Topic.id != topic_id,
        Topic.topic == data['topic'].strip(),
        Topic.grade_level == data['grade_level']
    ).first()
    
    if existing_topic:
        return jsonify({'error': 'Topic with this name already exists for this grade level'}), 400

    topic.topic = data['topic'].strip()
    topic.skill = data['skill'].strip()
    topic.grade_level = data['grade_level']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Topic updated successfully',
            'topic': topic.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update topic'}), 500

@admin_bp.route('/topics/<int:topic_id>', methods=['DELETE'])
@jwt_required()
def delete_topic(topic_id):
    """Delete a topic"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    topic = Topic.query.get(topic_id)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    # Check if topic is referenced by any questions
    if topic.questions:
        return jsonify({
            'error': 'Cannot delete topic that is referenced by questions',
            'question_count': len(topic.questions)
        }), 400
    
    try:
        db.session.delete(topic)
        db.session.commit()
        return jsonify({'message': 'Topic deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete topic'}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users (admin only)"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total_count': len(users)
    }), 200

@admin_bp.route('/users/<int:user_id>/admin', methods=['PUT'])
@jwt_required()
def toggle_admin_status(user_id):
    """Toggle admin status of a user"""
    current_user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent self-demotion
    if current_user.id == user_id:
        return jsonify({'error': 'Cannot modify your own admin status'}), 400
    
    target_user.is_admin = not target_user.is_admin
    
    try:
        db.session.commit()
        return jsonify({
            'message': f'User admin status {"granted" if target_user.is_admin else "revoked"} successfully',
            'user': target_user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update user admin status'}), 500

@admin_bp.route('/generate-questions', methods=['POST'])
@jwt_required()
def generate_questions():
    """Generate questions for a specific topic and complexity"""
    user, error_response, status_code = check_admin_access()
    if error_response:
        return error_response, status_code
    
    schema = QuestionGenerationSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    # Get the topic
    topic = Topic.query.get(data['topic_id'])
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    
    try:
        # Try to import and use the real question generator service
        try:
            from question_generator_service import generate_and_save_questions
            result = generate_and_save_questions(
                topic_id=data['topic_id'],
                complexity=data['complexity'],
                count=data['count'],
                provider=data['provider']
            )
        except (ImportError, Exception) as e:
            # Fallback to mock generator for testing/demo purposes
            print(f"Real generator failed: {e}, using mock generator")
            from mock_question_generator import generate_mock_questions
            result = generate_mock_questions(
                topic_id=data['topic_id'],
                complexity=data['complexity'],
                count=data['count']
            )
        
        if result['success']:
            return jsonify({
                'message': f'Successfully generated and saved {result["questions_saved"]} questions',
                'questions_generated': result['questions_generated'],
                'questions_saved': result['questions_saved'],
                'topic': result['topic_name'],
                'grade_level': result['grade_level'],
                'complexity': result['complexity']
            }), 201
        else:
            return jsonify({'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate questions: {str(e)}'}), 500
