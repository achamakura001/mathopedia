from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime
from app.database import get_db
from app.models import Question, UserAnswer, User, PracticeTest
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
                ~Question.id.in_(answered_question_ids.select())
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
    
    # Save selected questions to practice_test table
    try:
        test_date = datetime.utcnow()
        # Create test identifier from current time (HH:MM format)
        test_identifier = str(int(test_date.timestamp()))
        
        for question in selected_questions:
            practice_test = PracticeTest(
                test_date=test_date,
                test_identifier=test_identifier,
                user_id=current_user.id,
                question_id=question.id,
                grade_level=grade_filter,
                status=False  # Not attempted yet
            )
            db.add(practice_test)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create practice test: {str(e)}"
        )
    
    # Return questions without correct answers (for security)
    questions_data = []
    for question in selected_questions:
        question_dict = question.to_dict()
        question_dict['test_identifier'] = test_identifier
        # Remove correct answer from response
        question_dict.pop('correct_answer', None)
        question_dict.pop('explanation', None)
        questions_data.append(question_dict)
    
    return {
        'questions': questions_data,
        'total_count': len(questions_data),
        'test_identifier': test_identifier,
        'test_date': test_date.isoformat()
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


@router.get("/practice-tests/{grade_level}")
def get_practice_tests(
    grade_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: bool = Query(None, description="Filter by status")
):
    """Get practice tests for a specific grade"""
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
    
    # Build query
    query = db.query(PracticeTest).filter(
        and_(
            PracticeTest.user_id == current_user.id,
            PracticeTest.grade_level == grade_filter
        )
    )
    
    # Apply status filter if provided
    if status_filter is not None:
        query = query.filter(PracticeTest.status == status_filter)
    
    practice_tests = query.order_by(PracticeTest.test_date.desc()).all()
    
    return {
        'practice_tests': [test.to_dict() for test in practice_tests],
        'total_count': len(practice_tests)
    }


@router.get("/practice-tests/identifier/{test_identifier}")
def get_practice_test_by_identifier(
    test_identifier: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get practice test by test identifier"""
    practice_tests = db.query(PracticeTest).filter(
        and_(
            PracticeTest.user_id == current_user.id,
            PracticeTest.test_identifier == test_identifier
        )
    ).order_by(PracticeTest.created_at.asc()).all()
    
    if not practice_tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice test not found"
        )
    
    return {
        'practice_tests': [test.to_dict() for test in practice_tests],
        'total_count': len(practice_tests),
        'test_identifier': test_identifier
    }


@router.put("/practice-tests/{test_id}/complete")
def complete_practice_test(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a practice test as completed"""
    practice_test = db.query(PracticeTest).filter(
        and_(
            PracticeTest.id == test_id,
            PracticeTest.user_id == current_user.id
        )
    ).first()
    
    if not practice_test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice test not found"
        )
    
    try:
        practice_test.status = True
        db.commit()
        
        return {
            "message": "Practice test marked as completed",
            "practice_test": practice_test.to_dict()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update practice test: {str(e)}"
        )
