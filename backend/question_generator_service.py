"""
Enhanced question generator for Mathopedia admin panel
"""
import os
import sys

# Add the backend directory to the path so we can import our models
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

def generate_and_save_questions(topic_id, complexity, count, provider='ollama'):
    """
    Generate questions for a specific topic and save them to the database
    
    Args:
        topic_id (int): ID of the topic from Topics table
        complexity (str): Question complexity ('easy', 'medium', 'hard')
        count (int): Number of questions to generate
        provider (str): LLM provider ('ollama' or 'openai')
    
    Returns:
        dict: Result with success/error status and details
    """
    try:
        from app import create_app, db
        from app.models import Topic, Question
        from question_generator import LLMQuestionGenerator
        
        app = create_app()
        
        with app.app_context():
            # Get the topic
            topic = Topic.query.get(topic_id)
            if not topic:
                return {'success': False, 'error': 'Topic not found'}
            
            # Initialize generator
            generator = LLMQuestionGenerator()
            
            # Generate questions
            questions = generator.generate_questions(
                grade_level=topic.grade_level,
                topic=topic.name,
                complexity=complexity,
                count=count,
                provider=provider,
                skill_description=topic.skill
            )
            
            if not questions:
                return {'success': False, 'error': 'Failed to generate questions'}
            
            # Save to database
            saved_count = 0
            for question_data in questions:
                # Check if question already exists
                existing = Question.query.filter_by(
                    grade_level=question_data.grade_level,
                    question_text=question_data.question_text
                ).first()
                
                if not existing:
                    question = Question(
                        grade_level=question_data.grade_level,
                        complexity=question_data.complexity,
                        topic=question_data.topic,
                        topic_id=topic.id,  # Link to the topic
                        question_text=question_data.question_text,
                        correct_answer=question_data.correct_answer,
                        explanation=question_data.explanation
                    )
                    db.session.add(question)
                    saved_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'questions_generated': len(questions),
                'questions_saved': saved_count,
                'topic_name': topic.name,
                'grade_level': topic.grade_level,
                'complexity': complexity
            }
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Command-line usage
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate questions for Mathopedia')
    parser.add_argument('--topic-id', type=int, required=True, help='Topic ID from database')
    parser.add_argument('--complexity', type=str, required=True, choices=['easy', 'medium', 'hard'], help='Question complexity')
    parser.add_argument('--count', type=int, default=5, help='Number of questions to generate')
    parser.add_argument('--provider', type=str, default='ollama', choices=['ollama', 'openai'], help='LLM provider')
    
    args = parser.parse_args()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    result = generate_and_save_questions(
        topic_id=args.topic_id,
        complexity=args.complexity,
        count=args.count,
        provider=args.provider
    )
    
    if result['success']:
        print(f"✅ Successfully generated {result['questions_generated']} questions")
        print(f"📝 Saved {result['questions_saved']} new questions to database")
        print(f"📚 Topic: {result['topic_name']} (Grade {result['grade_level']})")
        print(f"⚡ Complexity: {result['complexity']}")
    else:
        print(f"❌ Error: {result['error']}")
