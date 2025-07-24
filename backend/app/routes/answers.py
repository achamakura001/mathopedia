from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from datetime import datetime, date
from app import db
from app.models import Question, UserAnswer, DailyProgress
from app.utils import get_current_user_id

answers_bp = Blueprint('answers', __name__)

class SubmitAnswerSchema(Schema):
    question_id = fields.Int(required=True)
    user_answer = fields.Str(required=True)

@answers_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_answer():
    """Submit an answer to a question"""
    schema = SubmitAnswerSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
        
    question_id = data['question_id']
    user_answer = data['user_answer'].strip()
    
    # Get the question
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Check if user has already answered this question
    existing_answer = UserAnswer.query.filter_by(
        user_id=current_user_id,
        question_id=question_id
    ).first()
    
    if existing_answer:
        return jsonify({'error': 'Question already answered'}), 400
    
    # Check if answer is correct (case-insensitive comparison)
    is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
    
    # Create user answer record
    user_answer_record = UserAnswer(
        user_id=current_user_id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct
    )
    
    try:
        db.session.add(user_answer_record)
        
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
        
        # Return result with explanation
        response = {
            'message': 'Answer submitted successfully',
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'user_answer': user_answer
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit answer'}), 500

@answers_bp.route('/history', methods=['GET'])
@jwt_required()
def get_answer_history():
    """Get user's answer history"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    grade_level = request.args.get('grade_level', type=int)
    
    # Build query
    query = UserAnswer.query.filter_by(user_id=current_user_id)
    
    if grade_level:
        query = query.join(Question).filter(Question.grade_level == grade_level)
    
    # Order by most recent first
    query = query.order_by(UserAnswer.answered_at.desc())
    
    # Paginate
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    answers = [answer.to_dict() for answer in pagination.items]
    
    return jsonify({
        'answers': answers,
        'pagination': {
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

@answers_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_answer_stats():
    """Get overall answer statistics for the user"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Total answers
    total_answers = UserAnswer.query.filter_by(user_id=current_user_id).count()
    
    # Correct answers
    correct_answers = UserAnswer.query.filter_by(
        user_id=current_user_id,
        is_correct=True
    ).count()
    
    # Accuracy
    accuracy = round(correct_answers / total_answers * 100, 2) if total_answers > 0 else 0
    
    # Stats by grade
    grade_stats = []
    for grade in range(1, 13):
        grade_total = db.session.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == current_user_id,
            Question.grade_level == grade
        ).count()
        
        grade_correct = db.session.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == current_user_id,
            UserAnswer.is_correct == True,
            Question.grade_level == grade
        ).count()
        
        if grade_total > 0:
            grade_stats.append({
                'grade': grade,
                'total_answered': grade_total,
                'correct_answers': grade_correct,
                'accuracy': round(grade_correct / grade_total * 100, 2)
            })
    
    return jsonify({
        'total_answers': total_answers,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'grade_stats': grade_stats
    }), 200
