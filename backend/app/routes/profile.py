from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, timedelta
from sqlalchemy import func, distinct
from app import db
from app.models import User, DailyProgress, UserAnswer, Question, Topic
from app.utils import get_current_user_id

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile with comprehensive stats"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Basic user info
    profile_data = user.to_dict()
    
    # Calculate overall stats
    total_questions = UserAnswer.query.filter_by(user_id=current_user_id).count()
    correct_answers = UserAnswer.query.filter_by(
        user_id=current_user_id,
        is_correct=True
    ).count()
    
    overall_accuracy = round(correct_answers / total_questions * 100, 2) if total_questions > 0 else 0
    
    # Get daily progress for last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)
    daily_progress = DailyProgress.query.filter(
        DailyProgress.user_id == current_user_id,
        DailyProgress.date >= thirty_days_ago
    ).order_by(DailyProgress.date.asc()).all()
    
    # Calculate streak (consecutive days of activity)
    current_streak = 0
    check_date = date.today()
    while True:
        progress_for_date = next(
            (p for p in daily_progress if p.date == check_date),
            None
        )
        if progress_for_date and progress_for_date.questions_answered > 0:
            current_streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    # Grade-wise performance - get all distinct grade levels from topics table
    available_grades = db.session.query(distinct(Topic.grade_level)).order_by(Topic.grade_level).all()
    grade_performance = []
    
    for (grade_level,) in available_grades:
        # Get all user answers for this grade level
        # Join topics and questions by grade_level and topic columns as requested
        grade_answers = db.session.query(UserAnswer).join(Question).join(
            Topic, 
            db.and_(
                Question.grade_level == Topic.grade_level,
                Question.topic == Topic.topic
            )
        ).filter(
            UserAnswer.user_id == current_user_id,
            Topic.grade_level == grade_level
        ).all()
        
        if grade_answers:
            grade_correct = sum(1 for answer in grade_answers if answer.is_correct)
            
            # Format grade display name - prefix numeric grades with "Grade"
            if grade_level.isdigit():
                grade_display = f"Grade {grade_level}"
            else:
                grade_display = grade_level  # Display as-is for non-numeric (e.g., "Competitive Exams")
            
            grade_performance.append({
                'grade_level': grade_level,
                'grade_display': grade_display,
                'total_questions': len(grade_answers),
                'correct_answers': grade_correct,
                'accuracy': round(grade_correct / len(grade_answers) * 100, 2)
            })
    
    profile_data.update({
        'stats': {
            'total_questions_answered': total_questions,
            'correct_answers': correct_answers,
            'overall_accuracy': overall_accuracy,
            'current_streak': current_streak,
            'total_study_days': len([p for p in daily_progress if p.questions_answered > 0])
        },
        'daily_progress': [progress.to_dict() for progress in daily_progress],
        'grade_performance': grade_performance
    })
    
    return jsonify(profile_data), 200

@profile_bp.route('/daily-progress', methods=['GET'])
@jwt_required()
def get_daily_progress():
    """Get daily progress for a specific date range"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Get date range from query parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = date.today() - timedelta(days=30)
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = date.today()
    
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Query daily progress
    progress_records = DailyProgress.query.filter(
        DailyProgress.user_id == current_user_id,
        DailyProgress.date >= start_date,
        DailyProgress.date <= end_date
    ).order_by(DailyProgress.date.asc()).all()
    
    return jsonify({
        'daily_progress': [record.to_dict() for record in progress_records],
        'date_range': {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    }), 200

@profile_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    """Get user achievements and milestones"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Calculate various achievements
    total_questions = UserAnswer.query.filter_by(user_id=current_user_id).count()
    correct_answers = UserAnswer.query.filter_by(
        user_id=current_user_id,
        is_correct=True
    ).count()
    
    # Study streak
    daily_records = DailyProgress.query.filter_by(user_id=current_user_id).all()
    study_days = len([r for r in daily_records if r.questions_answered > 0])
    
    # Perfect scores (100% accuracy days)
    perfect_days = len([r for r in daily_records if r.questions_answered > 0 and r.correct_answers == r.questions_answered])
    
    achievements = []
    
    # Question milestones
    question_milestones = [10, 50, 100, 250, 500, 1000]
    for milestone in question_milestones:
        if total_questions >= milestone:
            achievements.append({
                'title': f'{milestone} Questions Answered',
                'description': f'You have answered {milestone} questions!',
                'type': 'milestone',
                'earned': True,
                'date_earned': None  # Could be tracked if we store achievement dates
            })
    
    # Accuracy achievements
    overall_accuracy = round(correct_answers / total_questions * 100, 2) if total_questions > 0 else 0
    if overall_accuracy >= 90 and total_questions >= 50:
        achievements.append({
            'title': 'Math Genius',
            'description': 'Maintain 90%+ accuracy with 50+ questions',
            'type': 'accuracy',
            'earned': True
        })
    
    # Streak achievements
    streak_milestones = [3, 7, 14, 30]
    for milestone in streak_milestones:
        if study_days >= milestone:
            achievements.append({
                'title': f'{milestone} Day Scholar',
                'description': f'Study for {milestone} consecutive days',
                'type': 'streak',
                'earned': True
            })
    
    # Perfect day achievements
    if perfect_days >= 5:
        achievements.append({
            'title': 'Perfectionist',
            'description': 'Achieve 100% accuracy on 5 different days',
            'type': 'perfect',
            'earned': True
        })
    
    return jsonify({
        'achievements': achievements,
        'stats': {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'overall_accuracy': overall_accuracy,
            'study_days': study_days,
            'perfect_days': perfect_days
        }
    }), 200

@profile_bp.route('/grade/<grade_level>/topics', methods=['GET'])
@jwt_required()
def get_grade_topic_performance(grade_level):
    """Get topic-wise performance breakdown for a specific grade"""
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    # Get all topics for the specified grade level
    topics = Topic.query.filter_by(grade_level=grade_level).all()
    
    if not topics:
        return jsonify({'error': f'No topics found for grade level: {grade_level}'}), 404
    
    topic_performance = []
    
    for topic in topics:
        # Get user answers for questions in this topic and grade level
        # Join UserAnswer -> Question -> Topic by grade_level and topic
        user_answers = db.session.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == current_user_id,
            Question.grade_level == grade_level,
            Question.topic == topic.topic
        ).all()
        
        if user_answers:
            correct_answers = sum(1 for answer in user_answers if answer.is_correct)
            total_questions = len(user_answers)
            accuracy = round(correct_answers / total_questions * 100, 2)
        else:
            correct_answers = 0
            total_questions = 0
            accuracy = 0
        
        topic_performance.append({
            'topic_id': topic.id,
            'topic_name': topic.topic,
            'skill': topic.skill,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': accuracy
        })
    
    # Sort by accuracy descending, then by total questions descending
    topic_performance.sort(key=lambda x: (x['accuracy'], x['total_questions']), reverse=True)
    
    # Format grade display name
    if grade_level.isdigit():
        grade_display = f"Grade {grade_level}"
    else:
        grade_display = grade_level
    
    return jsonify({
        'grade_level': grade_level,
        'grade_display': grade_display,
        'topic_performance': topic_performance,
        'total_topics': len(topics),
        'topics_attempted': len([t for t in topic_performance if t['total_questions'] > 0])
    }), 200
