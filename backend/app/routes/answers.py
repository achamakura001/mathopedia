from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models import Question, UserAnswer, DailyProgress, User
from app.schemas import AnswerSubmit
from app.auth import get_current_user

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post("/submit")
def submit_answer(
    answer_data: AnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit an answer to a question"""
    question_id = answer_data.question_id
    user_answer = answer_data.user_answer.strip()
    
    # Get the question
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Question not found'
        )
    
    # Check if user has already answered this question
    existing_answer = db.query(UserAnswer).filter(
        UserAnswer.user_id == current_user.id,
        UserAnswer.question_id == question_id
    ).first()
    
    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Question already answered'
        )
    
    # Check if answer is correct (case-insensitive comparison)
    is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
    
    # Create user answer record
    user_answer_record = UserAnswer(
        user_id=current_user.id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct
    )
    
    try:
        db.add(user_answer_record)
        db.commit()
        db.refresh(user_answer_record)
        
        # Update daily progress
        today = date.today()
        progress = db.query(DailyProgress).filter(
            DailyProgress.user_id == current_user.id,
            DailyProgress.date == today
        ).first()
        
        if not progress:
            progress = DailyProgress(
                user_id=current_user.id,
                date=today,
                questions_answered=1,
                correct_answers=1 if is_correct else 0
            )
            db.add(progress)
        else:
            progress.questions_answered += 1
            if is_correct:
                progress.correct_answers += 1
        
        db.commit()
        
        return {
            'message': 'Answer submitted successfully',
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'answer_id': user_answer_record.id
        }
        
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to submit answer'
        )


@router.get("/history")
def get_answer_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get user's answer history"""
    answers = db.query(UserAnswer).filter(
        UserAnswer.user_id == current_user.id
    ).order_by(UserAnswer.answered_at.desc()).offset(skip).limit(limit).all()
    
    return {
        'answers': [answer.to_dict() for answer in answers],
        'total_count': len(answers)
    }

@router.get("/stats")
def get_answer_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("parsing /stats")
    """Get overall answer statistics for the user"""
    current_user_id = current_user.id
    
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user authentication"
        )
    
    # Total answers
    user_answers = db.query(UserAnswer).filter_by(user_id=current_user_id).all()
    total_answers = len(user_answers)
    
    # Correct answers
    correct_answers = len([answer for answer in user_answers if answer.is_correct])

    
    # Accuracy
    accuracy = round(correct_answers / total_answers * 100, 2) if total_answers > 0 else 0
    print(current_user.id, accuracy, total_answers, correct_answers)
    # Stats by grade
    grade_stats = []
    for grade in range(1, 13):
        grade_answers = db.query(UserAnswer).join(Question).filter(
            UserAnswer.user_id == current_user_id,
            Question.grade_level == str(grade)
        ).all()
        grade_total = len(grade_answers)
        # grade_total = db.session.query(UserAnswer).join(Question).filter(
        #     UserAnswer.user_id == current_user_id,
        #     Question.grade_level == grade
        # ).count()
        
        grade_correct = len([answer for answer in grade_answers if answer.is_correct])
        # grade_correct = db.session.query(UserAnswer).join(Question).filter(
        #     UserAnswer.user_id == current_user_id,
        #     UserAnswer.is_correct == True,
        #     Question.grade_level == grade
        # ).count()
        
        if grade_total > 0:
            grade_stats.append({
                'grade': grade,
                'total_answered': grade_total,
                'correct_answers': grade_correct,
                'accuracy': round(grade_correct / grade_total * 100, 2)
            })
    
    return {
            'total_answers': total_answers,
            'correct_answers': correct_answers,
            'accuracy': accuracy,
            'grade_stats': grade_stats
            }
        

@router.get("/{answer_id}")
def get_answer(
    answer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print("Get answer")
    """Get a specific answer by ID"""
    answer = db.query(UserAnswer).filter(
        UserAnswer.id == answer_id,
        UserAnswer.user_id == current_user.id
    ).first()
    
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Answer not found'
        )
    
    return {'answer': answer.to_dict()}
