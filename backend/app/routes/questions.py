from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_, func
from app import db
from app.models import Question, UserAnswer
from app.utils import get_current_user_id
import random

questions_bp = Blueprint('questions', __name__)

@questions_bp.route('/grade/<grade_level>', methods=['GET'])
@jwt_required()
def get_questions_for_grade(grade_level):
    """Get 10 random questions for a specific grade that the user hasn't answered"""
    try:
        # Handle both numeric grades and competitive exams
        if grade_level == "competitive":
            grade_filter = "Competitive Exams"
        else:
            try:
                grade_int = int(grade_level)
                if grade_int < 1 or grade_int > 12:
                    return jsonify({'error': 'Invalid grade level. Must be between 1 and 12 or "competitive"'}), 400
                grade_filter = str(grade_int)
            except ValueError:
                return jsonify({'error': 'Invalid grade level. Must be between 1 and 12 or "competitive"'}), 400
        
        current_user_id = get_current_user_id()
        
        if not current_user_id:
            return jsonify({'error': 'Invalid user authentication'}), 401
        
        # Get question IDs that the user has already answered
        answered_question_ids = db.session.query(UserAnswer.question_id)\
            .filter_by(user_id=current_user_id)\
            .subquery()
        
        # Get questions for the grade that haven't been answered by the user
        available_questions = Question.query\
            .filter(
                and_(
                    Question.grade_level == grade_filter,
                    ~Question.id.in_(answered_question_ids)
                )
            )\
            .all()
        
        if not available_questions:
            return jsonify({'error': 'No more questions available for this grade'}), 404
        
        # For competitive exams, questions are all medium complexity
        if grade_filter == "Competitive Exams":
            # Select up to 10 random questions
            selected_questions = random.sample(available_questions, min(10, len(available_questions)))
        else:
            # Original complexity distribution for regular grades
            # Try to get a mix of complexities
            easy_questions = [q for q in available_questions if q.complexity == 'easy']
            medium_questions = [q for q in available_questions if q.complexity == 'medium']
            hard_questions = [q for q in available_questions if q.complexity == 'hard']
            
            selected_questions = []
            
            # Distribute questions: 4 easy, 4 medium, 2 hard (if available)
            selected_questions.extend(random.sample(easy_questions, min(4, len(easy_questions))))
            selected_questions.extend(random.sample(medium_questions, min(4, len(medium_questions))))
            selected_questions.extend(random.sample(hard_questions, min(2, len(hard_questions))))
            
            # If we don't have enough questions, fill from remaining
            if len(selected_questions) < 10:
                remaining_questions = [q for q in available_questions if q not in selected_questions]
                additional_needed = min(10 - len(selected_questions), len(remaining_questions))
                selected_questions.extend(random.sample(remaining_questions, additional_needed))
        
        # Shuffle the final selection
        random.shuffle(selected_questions)
        
        # Return questions without correct answers (for security)
        questions_data = []
        for question in selected_questions:
            question_dict = question.to_dict()
            # Remove correct answer from response
            question_dict.pop('correct_answer', None)
            question_dict.pop('explanation', None)
            questions_data.append(question_dict)
        
        return jsonify({
            'questions': questions_data,
            'total_count': len(questions_data)
        }), 200
        
    except Exception as e:
        print(f"Error in get_questions_for_grade: {str(e)}")  # Server-side logging
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@questions_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    """Get a specific question"""
    question = Question.query.get(question_id)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Return question without correct answer
    question_dict = question.to_dict()
    question_dict.pop('correct_answer', None)
    question_dict.pop('explanation', None)
    
    return jsonify({'question': question_dict}), 200

@questions_bp.route('/stats/grade/<grade_level>', methods=['GET'])
@jwt_required()
def get_grade_stats(grade_level):
    """Get statistics for a specific grade"""
    # Handle both numeric grades and competitive exams
    if grade_level == "competitive":
        grade_filter = "Competitive Exams"
    else:
        try:
            grade_int = int(grade_level)
            if grade_int < 1 or grade_int > 12:
                return jsonify({'error': 'Invalid grade level. Must be between 1 and 12 or "competitive"'}), 400
            grade_filter = str(grade_int)
        except ValueError:
            return jsonify({'error': 'Invalid grade level. Must be between 1 and 12 or "competitive"'}), 400
    
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Total questions available for this grade
    total_questions = Question.query.filter_by(grade_level=grade_filter).count()
    
    # Questions answered by user for this grade
    answered_questions = db.session.query(func.count(UserAnswer.id))\
        .join(Question)\
        .filter(
            and_(
                UserAnswer.user_id == current_user_id,
                Question.grade_level == grade_filter
            )
        ).scalar()
    
    # Correct answers by user for this grade
    correct_answers = db.session.query(func.count(UserAnswer.id))\
        .join(Question)\
        .filter(
            and_(
                UserAnswer.user_id == current_user_id,
                Question.grade_level == grade_filter,
                UserAnswer.is_correct == True
            )
        ).scalar()
    
    accuracy = round(correct_answers / answered_questions * 100, 2) if answered_questions > 0 else 0
    
    return jsonify({
        'grade_level': grade_level,
        'total_questions': total_questions,
        'answered_questions': answered_questions,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'remaining_questions': total_questions - answered_questions
    }), 200
