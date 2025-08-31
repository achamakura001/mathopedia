from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.database import get_db
from app.models import User, Question, Topic
from app.schemas import GenerateQuestions, QuestionCreate, TopicCreate
from app.auth import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])



@router.get("/users")
def get_all_users(
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    total_count = db.query(User).count()
    return {
        "users": [user.to_dict() for user in users],
        "total_count": total_count
    }




@router.get("/topics")
def get_all_topics(
    grade_level: Optional[str] = Query(None, description="Filter by grade level"),
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all topics across all grades with question statistics (admin only)"""
    try:
        # Build query with optional grade level filter
        query = db.query(Topic)
        if grade_level:
            query = query.filter(Topic.grade_level == grade_level)
        
        topics = query.order_by(Topic.grade_level, Topic.topic).all()
        
        # Get question statistics for each topic
        topics_with_stats = []
        for topic in topics:
            topic_dict = topic.to_dict()
            
            # Get question counts by complexity for this topic and grade
            question_stats = db.query(
                Question.complexity,
                func.count(Question.id).label('count')
            ).filter(
                Question.topic_id == topic.id
            ).group_by(Question.complexity).all()
            
            # Also check for questions that reference this topic by string (backward compatibility)
            legacy_question_stats = db.query(
                Question.complexity,
                func.count(Question.id).label('count')
            ).filter(
                Question.topic == topic.topic,
                Question.grade_level == str(topic.grade_level),
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
        
        return {
            'topics': topics_with_stats,
            'total_count': len(topics),
            'filtered_by_grade': grade_level
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch topics: {str(e)}"
        )



@router.post("/topics")
def create_topic(
    topic_data: TopicCreate,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new topic (admin only)"""
    if not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )

    try:
        # Check if topic already exists for this grade level
        existing_topic = db.query(Topic).filter(
            Topic.topic == topic_data.topic,
            Topic.grade_level == topic_data.grade_level
        ).first()
        
        if existing_topic:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Topic already exists for this grade level"
            )
        
        topic = Topic(**topic_data.model_dump())
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return {"message": "Topic created successfully", "topic": topic.to_dict()}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create topic: {str(e)}"
        )


@router.put("/topics/{topic_id}")
def update_topic(
    topic_id: int,
    topic_data: TopicCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update an existing topic (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        

        print("Trying to update ....")
        # Update topic fields
        topic.topic = topic_data.topic
        topic.skill = topic_data.skill
        topic.grade_level = topic_data.grade_level
        db.commit()
        db.refresh(topic)
        
        return {"message": "Topic updated successfully", "topic": topic.to_dict()}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update topic: {str(e)}"
        )


@router.delete("/topics/{topic_id}")
def delete_topic(
    topic_id: int,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a topic (admin only)"""
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        
        # Check if topic has associated questions
        question_count = db.query(Question).filter(Question.topic_id == topic_id).count()
        if question_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete topic with {question_count} associated questions"
            )
        
        db.delete(topic)
        db.commit()
        
        return {"message": "Topic deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete topic: {str(e)}"
        )


@router.post("/questions")
def create_question(
    question_data: QuestionCreate,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new question (admin only)"""
    question = Question(**question_data.model_dump())
    
    try:
        db.add(question)
        db.commit()
        db.refresh(question)
        return {"message": "Question created successfully", "question": question.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create question: {str(e)}"
        )

@router.post("/generate-questions")
def generate_questions(
    i_topic: GenerateQuestions,
    admin_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Generate questions for a specific topic and complexity (admin only)"""
    try:
        print("Generating questions...")
        # Validate complexity
        if i_topic.complexity not in ['easy', 'medium', 'hard']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Complexity must be 'easy', 'medium', or 'hard'"
            )
        
        # Validate count
        if not 1 <= i_topic.count <= 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Count must be between 1 and 20"
            )
        
        # Get the topic
        topic = db.query(Topic).filter(Topic.id == i_topic.topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topic not found"
            )
        
        # Mock response for now (replace with actual question generation logic)
        return {
            'message': f'Successfully generated {i_topic.count} questions',
            'questions_generated': i_topic.count,
            'questions_saved': i_topic.count,
            'topic': topic.topic,
            'grade_level': topic.grade_level,
            'complexity': i_topic.complexity,
            'provider': i_topic.provider
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}"
        )
    
