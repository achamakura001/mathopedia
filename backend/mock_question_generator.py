"""
Mock question generator for testing purposes when LLM services are not available
"""
import sys
import os

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_path)

def generate_mock_questions(topic_id, complexity, count):
    """Generate mock questions for testing"""
    try:
        from app import create_app, db
        from app.models import Topic, Question
        
        app = create_app()
        
        with app.app_context():
            # Get the topic
            topic = Topic.query.get(topic_id)
            if not topic:
                return {'success': False, 'error': 'Topic not found'}
            
            # Generate mock questions based on topic and complexity
            mock_questions = []
            
            for i in range(count):
                if topic.name.lower() == 'fractions':
                    if complexity == 'easy':
                        mock_questions.append({
                            'question_text': f'What is 1/{i+2} + 1/{i+4}?',
                            'correct_answer': f'{(i+4+i+2)}/{(i+2)*(i+4)}',
                            'explanation': f'To add fractions, find a common denominator. The common denominator of {i+2} and {i+4} is {(i+2)*(i+4)}.'
                        })
                    elif complexity == 'medium':
                        mock_questions.append({
                            'question_text': f'Simplify {2*(i+1)}/{4*(i+1)}',
                            'correct_answer': '1/2',
                            'explanation': f'Cancel the common factor {i+1} from numerator and denominator: {2*(i+1)}/{4*(i+1)} = 2/4 = 1/2'
                        })
                    else:  # hard
                        mock_questions.append({
                            'question_text': f'A recipe calls for {i+1}/3 cups of flour and {i+2}/6 cups of sugar. How much more flour than sugar is needed?',
                            'correct_answer': f'{2*(i+1)-(i+2)}/6 cups',
                            'explanation': f'Convert {i+1}/3 to sixths: {2*(i+1)}/6. Subtract: {2*(i+1)}/6 - {i+2}/6 = {2*(i+1)-(i+2)}/6'
                        })
                elif topic.name.lower() == 'decimals':
                    if complexity == 'easy':
                        mock_questions.append({
                            'question_text': f'What is {i+1}.5 + {i+2}.3?',
                            'correct_answer': f'{(i+1) + (i+2) + 0.8}',
                            'explanation': f'Add the whole numbers: {i+1} + {i+2} = {i+1+i+2}. Add the decimals: 0.5 + 0.3 = 0.8. Total: {(i+1) + (i+2) + 0.8}'
                        })
                    elif complexity == 'medium':
                        mock_questions.append({
                            'question_text': f'Round {(i+1)*1.234} to the nearest tenth.',
                            'correct_answer': f'{round((i+1)*1.234, 1)}',
                            'explanation': f'Look at the hundredths place to round to the nearest tenth. {(i+1)*1.234} rounds to {round((i+1)*1.234, 1)}'
                        })
                else:  # general topics
                    if complexity == 'easy':
                        mock_questions.append({
                            'question_text': f'Basic {topic.name} question {i+1}: What is a fundamental concept in {topic.name.lower()}?',
                            'correct_answer': f'Sample answer about {topic.name.lower()} concept {i+1}',
                            'explanation': f'This is a basic explanation of {topic.name.lower()} concepts for grade {topic.grade_level} students.'
                        })
                    elif complexity == 'medium':
                        mock_questions.append({
                            'question_text': f'Intermediate {topic.name} question {i+1}: Solve this {topic.name.lower()} problem step by step.',
                            'correct_answer': f'Solution {i+1} for {topic.name.lower()}',
                            'explanation': f'Step-by-step solution for this {complexity} level {topic.name.lower()} problem.'
                        })
                    else:  # hard
                        mock_questions.append({
                            'question_text': f'Advanced {topic.name} question {i+1}: Apply {topic.name.lower()} concepts to solve this complex problem.',
                            'correct_answer': f'Complex solution {i+1}',
                            'explanation': f'Detailed explanation for this {complexity} level {topic.name.lower()} problem requiring multiple steps.'
                        })
            
            # Save to database
            saved_count = 0
            for mock_q in mock_questions:
                # Check if question already exists
                existing = Question.query.filter_by(
                    grade_level=topic.grade_level,
                    question_text=mock_q['question_text']
                ).first()
                
                if not existing:
                    question = Question(
                        grade_level=topic.grade_level,
                        complexity=complexity,
                        topic=topic.name,
                        topic_id=topic.id,
                        question_text=mock_q['question_text'],
                        correct_answer=mock_q['correct_answer'],
                        explanation=mock_q['explanation']
                    )
                    db.session.add(question)
                    saved_count += 1
            
            db.session.commit()
            
            return {
                'success': True,
                'questions_generated': len(mock_questions),
                'questions_saved': saved_count,
                'topic_name': topic.name,
                'grade_level': topic.grade_level,
                'complexity': complexity
            }
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Test the mock generator
    result = generate_mock_questions(2, 'medium', 3)  # Fractions, medium, 3 questions
    print(result)
