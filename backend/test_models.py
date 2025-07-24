#!/usr/bin/env python3
"""
Test script to verify the updated Topic and Question models work correctly
"""

from app import create_app
from app.models import Topic, Question

def test_topic_question_relationship():
    app = create_app()
    with app.app_context():
        from app import db
        
        print("Testing Topic and Question relationship...")
        
        # Test 1: Create a topic with string grade_level
        print("\n1. Testing Topic creation with string grade_level:")
        
        try:
            # Create a topic for competitive exams
            competitive_topic = Topic(
                name="Advanced Calculus",
                skill="Understand limits, derivatives, and integrals at an advanced level",
                grade_level="Competitive Exams"
            )
            
            # Create a topic for grade 12
            grade12_topic = Topic(
                name="Trigonometry",
                skill="Master trigonometric functions and identities",
                grade_level="12"
            )
            
            db.session.add(competitive_topic)
            db.session.add(grade12_topic)
            db.session.commit()
            
            print(f"✓ Created competitive topic: {competitive_topic.to_dict()}")
            print(f"✓ Created grade 12 topic: {grade12_topic.to_dict()}")
            
        except Exception as e:
            print(f"✗ Error creating topics: {e}")
            db.session.rollback()
        
        # Test 2: Create questions and link them to topics
        print("\n2. Testing Question-Topic relationship:")
        
        try:
            # Create a question for competitive exams
            competitive_question = Question(
                grade_level="Competitive Exams",
                complexity="hard",
                topic="Advanced Calculus",
                question_text="Find the derivative of f(x) = x^3 * sin(x)",
                correct_answer="3x^2 * sin(x) + x^3 * cos(x)",
                explanation="Using the product rule: d/dx[u*v] = u'*v + u*v'"
            )
            
            # Create a question for grade 12
            grade12_question = Question(
                grade_level="12",
                complexity="medium",
                topic="Trigonometry",
                question_text="What is sin(π/4)?",
                correct_answer="√2/2",
                explanation="sin(π/4) = sin(45°) = √2/2"
            )
            
            db.session.add(competitive_question)
            db.session.add(grade12_question)
            db.session.commit()
            
            print(f"✓ Created competitive question: {competitive_question.id}")
            print(f"✓ Created grade 12 question: {grade12_question.id}")
            
            # Test the automatic topic linking
            print("\n3. Testing automatic topic linking:")
            comp_dict = competitive_question.to_dict()
            grade12_dict = grade12_question.to_dict()
            
            print(f"✓ Competitive question topic_id: {comp_dict.get('topic_id')}")
            print(f"✓ Competitive question topic_ref: {comp_dict.get('topic_ref')}")
            print(f"✓ Grade 12 question topic_id: {grade12_dict.get('topic_id')}")
            print(f"✓ Grade 12 question topic_ref: {grade12_dict.get('topic_ref')}")
            
        except Exception as e:
            print(f"✗ Error creating/linking questions: {e}")
            db.session.rollback()
        
        # Test 3: Query topics by different grade levels
        print("\n4. Testing topic queries:")
        
        try:
            competitive_topics = Topic.query.filter_by(grade_level="Competitive Exams").all()
            grade12_topics = Topic.query.filter_by(grade_level="12").all()
            
            print(f"✓ Found {len(competitive_topics)} competitive topics")
            print(f"✓ Found {len(grade12_topics)} grade 12 topics")
            
            # Show some existing topics
            all_topics = Topic.query.limit(5).all()
            print(f"✓ Sample topics in database:")
            for topic in all_topics:
                print(f"  - {topic.name} (Grade: {topic.grade_level})")
                
        except Exception as e:
            print(f"✗ Error querying topics: {e}")
        
        print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_topic_question_relationship()
