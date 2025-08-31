from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserUpdate
from app.auth import get_current_user
from datetime import date, timedelta
from app.models import User, DailyProgress, UserAnswer, Question, Topic
import json
router = APIRouter(prefix="/profile", tags=["profile"])


@router.get('/achievements')
def get_achievements(current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db)):
    """Get user achievements and milestones"""
    current_user_id = current_user.id
    
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid user authentication")
    
    # Calculate various achievements
    user_answers = db.query(UserAnswer).filter_by(user_id=current_user_id).all()
    total_questions = len(user_answers)
    correct_answers = len([ans for ans in user_answers if ans.is_correct])
        
    # Study streak
    daily_records = db.query(DailyProgress).filter_by(user_id=current_user_id).all()
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
    
    return {
        'achievements': achievements,
        'stats': {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'overall_accuracy': overall_accuracy,
            'study_days': study_days,
            'perfect_days': perfect_days
        }
    }


@router.get("/")
def get_profile(current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    
    profile_data = current_user.to_dict()
    
    # Calculate overall stats
    userAnswers = db.query(UserAnswer).filter_by(user_id=current_user.id).all()
    total_questions = len(userAnswers)

    correct_answers = sum(1 for answer in userAnswers if answer.is_correct) 
    
    overall_accuracy = round(correct_answers / total_questions * 100, 2) if total_questions > 0 else 0
    
    print(total_questions, correct_answers, overall_accuracy)
    # Get daily progress for last 30 days
    thirty_days_ago = date.today() - timedelta(days=30)

    daily_progress = db.query(DailyProgress).filter(
        DailyProgress.user_id == current_user.id,
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
    available_grades = db.query(Topic.grade_level).order_by(Topic.grade_level).distinct().all()
    grade_performance = []
    
    for (grade_level,) in available_grades:
        # Get all user answers for this grade level
        # Join topics and questions by grade_level and topic columns as requested
        from sqlalchemy import and_
        grade_answers = db.query(UserAnswer).join(Question).join(
            Topic,
            and_(
                Question.grade_level == Topic.grade_level,
                Question.topic == Topic.topic
            )
        ).filter(
            UserAnswer.user_id == current_user.id,
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
    return profile_data


@router.put("/me")
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    update_data = user_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    try:
        db.commit()
        db.refresh(current_user)
        return {"message": "Profile updated successfully", "user": current_user.to_dict()}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.get("/progress")
def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    days: int = 7
):
    """Get user progress for the last N days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    progress_records = db.query(DailyProgress).filter(
        DailyProgress.user_id == current_user.id,
        DailyProgress.date >= start_date,
        DailyProgress.date <= end_date
    ).order_by(DailyProgress.date.desc()).all()
    
    return {
        "progress": [record.to_dict() for record in progress_records],
        "total_records": len(progress_records)
    }

