from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.database import get_db
from app.models import Question, UserAnswer, User
from app.auth import get_current_user
import random

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/grade/{grade_level}")
def get_questions_for_grade(
    grade_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    count: int = Query(10, ge=1, le=50, description="Number of questions to return")
):
    """Get random questions for a specific grade that the user hasn't answered"""
    # Handle both numeric grades and competitive exams
    if grade_level == "competitive":
        grade_filter = "Competitive Exams"
    else:
        try:
            grade_int = int(grade_level)
            if grade_int < 1 or grade_int > 12:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid grade level. Must be between 1 and 12 or "competitive"'
                )
            grade_filter = str(grade_int)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid grade level. Must be between 1 and 12 or "competitive"'
            )
    
    # Get question IDs that the user has already answered
    answered_question_ids = db.query(UserAnswer.question_id)\
        .filter_by(user_id=current_user.id)\
        .subquery()
    
    # Get questions for the grade that haven't been answered by the user
    available_questions = db.query(Question)\
        .filter(
            and_(
                Question.grade_level == grade_filter,
                ~Question.id.in_(answered_question_ids)
            )
        )\
        .all()
    
    if not available_questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No more questions available for this grade'
        )
    
    # For competitive exams, questions are all medium complexity
    if grade_filter == "Competitive Exams":
        # Select up to count random questions
        selected_questions = random.sample(available_questions, min(count, len(available_questions)))
    else:
        # Original complexity distribution for regular grades
        # Try to get a mix of complexities
        easy_questions = [q for q in available_questions if q.complexity == 'easy']
        medium_questions = [q for q in available_questions if q.complexity == 'medium']
        hard_questions = [q for q in available_questions if q.complexity == 'hard']
        
        selected_questions = []
        
        # Distribute questions proportionally
        easy_count = min(int(count * 0.4), len(easy_questions))
        medium_count = min(int(count * 0.4), len(medium_questions))
        hard_count = min(int(count * 0.2), len(hard_questions))
        
        selected_questions.extend(random.sample(easy_questions, easy_count))
        selected_questions.extend(random.sample(medium_questions, medium_count))
        selected_questions.extend(random.sample(hard_questions, hard_count))
        
        # If we don't have enough questions, fill from remaining
        if len(selected_questions) < count:
            remaining_questions = [q for q in available_questions if q not in selected_questions]
            additional_needed = min(count - len(selected_questions), len(remaining_questions))
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
    
    return {
        'questions': questions_data,
        'total_count': len(questions_data)
    }


@router.get("/{question_id}")
def get_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Question not found'
        )
    
    # Return question without correct answer
    question_dict = question.to_dict()
    question_dict.pop('correct_answer', None)
    question_dict.pop('explanation', None)
    
    return {'question': question_dict}


@router.get("/stats/grade/{grade_level}")
def get_grade_stats(
    grade_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific grade"""
    # Handle both numeric grades and competitive exams
    if grade_level == "competitive":
        grade_filter = "Competitive Exams"
    else:
        try:
            grade_int = int(grade_level)
            if grade_int < 1 or grade_int > 12:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid grade level. Must be between 1 and 12 or "competitive"'
                )
            grade_filter = str(grade_int)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid grade level. Must be between 1 and 12 or "competitive"'
            )
    
    # Total questions available for this grade
    total_questions = db.query(Question).filter(Question.grade_level == grade_filter).count()
    
    # Questions answered by user for this grade
    answered_questions = db.query(func.count(UserAnswer.id))\
        .join(Question)\
        .filter(
            and_(
                UserAnswer.user_id == current_user.id,
                Question.grade_level == grade_filter
            )
        ).scalar()
    
    # Correct answers by user for this grade
    correct_answers = db.query(func.count(UserAnswer.id))\
        .join(Question)\
        .filter(
            and_(
                UserAnswer.user_id == current_user.id,
                Question.grade_level == grade_filter,
                UserAnswer.is_correct == True
            )
        ).scalar()
    
    accuracy = round(correct_answers / answered_questions * 100, 2) if answered_questions > 0 else 0
    
    return {
        'grade_level': grade_level,
        'total_questions': total_questions,
        'answered_questions': answered_questions,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'remaining_questions': total_questions - answered_questions
    }
