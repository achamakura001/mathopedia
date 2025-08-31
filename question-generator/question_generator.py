import requests
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
import sys
import re

# Add the backend directory to the path so we can import our models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

@dataclass
class QuestionData:
    grade_level: int
    complexity: str
    topic: str
    question_text: str
    correct_answer: str
    explanation: str

class LLMQuestionGenerator:
    """Question generator that supports multiple LLM providers"""
    
    def __init__(self):
        self.ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'qwen2-math')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    
    def generate_questions_ollama(self, grade_level: int, topic: str, complexity: str, count: int = 5, skill_description: str = "") -> List[QuestionData]:
        """Generate questions using Ollama local LLM"""
        
        prompt = self._create_prompt(grade_level, topic, complexity, count, skill_description)
        
        payload = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 4096
            }
        }
        print("DEBUG: Ollama payload:", json.dumps(payload, indent=2))
        
        try:
            print("DEBUG: Sending request to Ollama...")
            response = requests.post(
                f"{self.ollama_base_url}/generate",
                json=payload,
                timeout=600
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get('response', '')
            
            print(f"DEBUG: Received response from Ollama (length: {len(generated_text)})")
            print(f"DEBUG: Raw response preview: {generated_text[:200]}...")
            
            questions = self._parse_questions(generated_text, grade_level, topic, complexity)
            print(f"DEBUG: Parsed {len(questions)} questions from Ollama response")
            
            return questions
            
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to call Ollama API: {e}")
            return []
        except Exception as e:
            print(f"ERROR: Failed to generate questions: {e}")
            return []
    
    def generate_questions_openai(self, grade_level: int, topic: str, complexity: str, count: int = 5, skill_description: str = "") -> List[QuestionData]:
        """Generate questions using OpenAI GPT"""
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")
        
        prompt = self._create_prompt(grade_level, topic, complexity, count, skill_description)
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a math teacher creating educational questions."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        print("DEBUG: OpenAI payload prepared")
        
        try:
            print("DEBUG: Sending request to OpenAI...")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content']
            
            print(f"DEBUG: Received response from OpenAI (length: {len(generated_text)})")
            print(f"DEBUG: Raw response preview: {generated_text[:200]}...")
            
            questions = self._parse_questions(generated_text, grade_level, topic, complexity)
            print(f"DEBUG: Parsed {len(questions)} questions from OpenAI response")
            
            return questions
            
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to call OpenAI API: {e}")
            return []
        except Exception as e:
            print(f"ERROR: Failed to generate questions: {e}")
            return []
    
    def _create_prompt(self, grade_level: int, topic: str, complexity: str, count: int, skill_description: str = "") -> str:
        """Create a structured prompt for question generation using template from common folder"""
        
        # Try to read the prompt template from common folder
        template_path = os.path.join(os.path.dirname(__file__), '..', 'common', 'question_generation_prompt.txt')
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Format the template with provided parameters
            return template.format(
                count=count,
                grade_level=grade_level,
                topic=topic,
                complexity=complexity,
                complexity_capitalized=complexity.capitalize(),
                skill_description=skill_description or f"Mathematical concepts related to {topic}"
            )
        except FileNotFoundError:
            # Fallback to original prompt if template file not found
            return f"""
Generate {count} math questions for grade {grade_level} students on the topic of {topic} with {complexity} complexity level.

For each question, provide:
1. Question text (clear and age-appropriate)
2. Correct answer (concise)
3. Detailed explanation (step-by-step solution)

Return your response as a valid JSON array containing exactly {count} question objects. Each object should have these exact keys:
- "question": the question text
- "answer": the correct answer
- "explanation": detailed step-by-step explanation

Example format:
[
  {{
    "question": "What is 2 + 3?",
    "answer": "5",
    "explanation": "To add 2 + 3, we start with 2 and count up 3 more: 3, 4, 5. So 2 + 3 = 5."
  }},
  {{
    "question": "What is 4 + 1?",
    "answer": "5", 
    "explanation": "To add 4 + 1, we start with 4 and add 1 more to get 5."
  }}
]

Guidelines:
- Grade {grade_level} appropriate language and concepts
- {complexity.capitalize()} difficulty level
- Focus on {topic}
- Include variety in question types
- Provide clear, educational explanations
- Use proper mathematical notation
- Return ONLY the JSON array, no additional text

Generate {count} questions now:
"""

    def _parse_questions(self, generated_text: str, grade_level: int, topic: str, complexity: str) -> List[QuestionData]:
        """Parse the generated text into structured question data"""
        
        questions = []
        
        print(f"DEBUG: Generated text length: {len(generated_text)}")
        print(f"DEBUG: First 500 characters of generated text:\n{generated_text[:500]}")
        
        # Clean up the response - remove any text before the first [ and after the last ]
        generated_text = generated_text.strip()
        
        # Find the JSON array boundaries
        start_bracket = generated_text.find('[')
        end_bracket = generated_text.rfind(']')
        
        if start_bracket == -1 or end_bracket == -1 or start_bracket >= end_bracket:
            print("DEBUG: No valid JSON array found in response")
            print("DEBUG: Looking for fallback patterns...")
            return self._parse_questions_fallback(generated_text, grade_level, topic, complexity)
        
        # Extract just the JSON array
        json_text = generated_text[start_bracket:end_bracket + 1]
        print(f"DEBUG: Extracted JSON text: {json_text[:200]}...")
        
        try:
            # Parse the JSON array
            questions_data = json.loads(json_text)
            
            if not isinstance(questions_data, list):
                print(f"DEBUG: Expected JSON array, got {type(questions_data)}")
                return self._parse_questions_fallback(generated_text, grade_level, topic, complexity)
            
            print(f"DEBUG: Successfully parsed JSON with {len(questions_data)} items")
            
            for i, item in enumerate(questions_data):
                if not isinstance(item, dict):
                    print(f"DEBUG: Item {i} is not a dictionary, skipping")
                    continue
                
                # Extract question data with flexible key names
                question_text = self._extract_field(item, ['question', 'Question', 'QUESTION', 'question_text'])
                correct_answer = self._extract_field(item, ['answer', 'Answer', 'ANSWER', 'correct_answer'])
                explanation = self._extract_field(item, ['explanation', 'Explanation', 'EXPLANATION'])
                
                if question_text and correct_answer and explanation:
                    # Clean up the text
                    question_text = str(question_text).strip()
                    correct_answer = str(correct_answer).strip()
                    explanation = str(explanation).strip()
                    
                    if question_text and correct_answer and explanation:
                        print(f"DEBUG: Successfully parsed question {i+1}: {question_text[:50]}...")
                        questions.append(QuestionData(
                            grade_level=grade_level,
                            complexity=complexity,
                            topic=topic,
                            question_text=question_text,
                            correct_answer=correct_answer,
                            explanation=explanation
                        ))
                else:
                    print(f"DEBUG: Item {i} missing required fields. Available keys: {list(item.keys())}")
            
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON parsing failed: {e}")
            print("DEBUG: Attempting fallback parsing...")
            return self._parse_questions_fallback(generated_text, grade_level, topic, complexity)
        except Exception as e:
            print(f"DEBUG: Unexpected error during JSON parsing: {e}")
            return self._parse_questions_fallback(generated_text, grade_level, topic, complexity)
        
        print(f"DEBUG: Total questions parsed: {len(questions)}")
        return questions
    
    def _extract_field(self, item: dict, possible_keys: List[str]) -> Optional[str]:
        """Extract a field from a dictionary using multiple possible key names"""
        for key in possible_keys:
            if key in item and item[key]:
                return item[key]
        return None
    
    def _parse_questions_fallback(self, generated_text: str, grade_level: int, topic: str, complexity: str) -> List[QuestionData]:
        """Fallback parsing method for non-JSON responses"""
        
        print("DEBUG: Using fallback parsing method...")
        questions = []
        
        # Try to find individual JSON objects in the text
        json_pattern = r'\{[^{}]*"(?:question|Question)"[^{}]*"(?:answer|Answer)"[^{}]*"(?:explanation|Explanation)"[^{}]*\}'
        json_matches = re.findall(json_pattern, generated_text, re.DOTALL | re.IGNORECASE)
        
        print(f"DEBUG: Found {len(json_matches)} potential JSON objects")
        
        for i, match in enumerate(json_matches):
            try:
                item = json.loads(match)
                question_text = self._extract_field(item, ['question', 'Question', 'QUESTION'])
                correct_answer = self._extract_field(item, ['answer', 'Answer', 'ANSWER'])
                explanation = self._extract_field(item, ['explanation', 'Explanation', 'EXPLANATION'])
                
                if question_text and correct_answer and explanation:
                    questions.append(QuestionData(
                        grade_level=grade_level,
                        complexity=complexity,
                        topic=topic,
                        question_text=str(question_text).strip(),
                        correct_answer=str(correct_answer).strip(),
                        explanation=str(explanation).strip()
                    ))
                    print(f"DEBUG: Fallback parsed question {i+1}")
            except:
                continue
        
        # If still no questions, try the old regex method
        if not questions:
            print("DEBUG: Trying old regex parsing method...")
            question_blocks = generated_text.split('---')
            
            for i, block in enumerate(question_blocks):
                block = block.strip()
                if not block:
                    continue
                
                # Simple regex patterns
                question_match = re.search(r'(?:QUESTION|question):\s*(.+?)(?=(?:ANSWER|answer):|$)', block, re.DOTALL | re.IGNORECASE)
                answer_match = re.search(r'(?:ANSWER|answer):\s*(.+?)(?=(?:EXPLANATION|explanation):|$)', block, re.DOTALL | re.IGNORECASE)
                explanation_match = re.search(r'(?:EXPLANATION|explanation):\s*(.+?)$', block, re.DOTALL | re.IGNORECASE)
                
                if question_match and answer_match and explanation_match:
                    question_text = question_match.group(1).strip()
                    correct_answer = answer_match.group(1).strip()
                    explanation = explanation_match.group(1).strip()
                    
                    # Clean up text
                    question_text = re.sub(r'\s+', ' ', question_text).strip()
                    correct_answer = re.sub(r'\s+', ' ', correct_answer).strip()
                    explanation = re.sub(r'\s+', ' ', explanation).strip()
                    
                    if question_text and correct_answer and explanation:
                        questions.append(QuestionData(
                            grade_level=grade_level,
                            complexity=complexity,
                            topic=topic,
                            question_text=question_text,
                            correct_answer=correct_answer,
                            explanation=explanation
                        ))
                        print(f"DEBUG: Regex parsed question {len(questions)}")
        
        print(f"DEBUG: Fallback parsing found {len(questions)} questions")
        return questions
    
    def generate_questions(self, grade_level: int, topic: str, complexity: str, count: int = 5, provider: str = 'ollama', skill_description: str = "") -> List[QuestionData]:
        """Generate questions using the specified provider"""
        
        if provider.lower() == 'ollama':
            return self.generate_questions_ollama(grade_level, topic, complexity, count, skill_description)
        elif provider.lower() == 'openai':
            return self.generate_questions_openai(grade_level, topic, complexity, count, skill_description)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

def save_questions_to_database(questions: List[QuestionData]):
    """Save generated questions to the database"""
    
    print(f"DEBUG: Attempting to save {len(questions)} questions to database")
    
    # Import here to avoid circular imports
    try:
        # Add backend to path if not already there
        backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        from app import create_app, db
        from app.models import Question
        
        print("DEBUG: Successfully imported database modules")
    except Exception as e:
        print(f"ERROR: Failed to import database modules: {e}")
        print("Make sure you're running this from the correct directory and the backend is set up properly")
        return
    
    app = create_app()
    
    with app.app_context():
        saved_count = 0
        skipped_count = 0
        
        for i, question_data in enumerate(questions):
            print(f"DEBUG: Processing question {i+1}: {question_data.question_text[:50]}...")
            
            # Check if question already exists
            existing = Question.query.filter_by(
                grade_level=question_data.grade_level,
                question_text=question_data.question_text
            ).first()
            
            if not existing:
                try:
                    question = Question(
                        grade_level=question_data.grade_level,
                        complexity=question_data.complexity,
                        topic=question_data.topic,
                        question_text=question_data.question_text,
                        correct_answer=question_data.correct_answer,
                        explanation=question_data.explanation
                    )
                    db.session.add(question)
                    saved_count += 1
                    print(f"DEBUG: Added question {i+1} to session")
                except Exception as e:
                    print(f"ERROR: Failed to create question object for question {i+1}: {e}")
            else:
                skipped_count += 1
                print(f"DEBUG: Question {i+1} already exists, skipping")
        
        try:
            db.session.commit()
            print(f"SUCCESS: Saved {saved_count} new questions to database!")
            if skipped_count > 0:
                print(f"INFO: Skipped {skipped_count} duplicate questions")
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Failed to save questions to database: {e}")
            print("This might be due to database connection issues or invalid data")
            raise

def debug_generation():
    """Debug function to test question generation without database operations"""
    from dotenv import load_dotenv
    load_dotenv()
    
    generator = LLMQuestionGenerator()
    
    print("=== DEBUG: Testing Question Generation ===")
    
    # Test with simple parameters
    questions = generator.generate_questions(
        grade_level=3,
        topic="Addition",
        complexity="easy",
        count=2,
        provider='ollama'
    )
    
    print(f"\n=== RESULTS ===")
    print(f"Generated {len(questions)} questions")
    
    if questions:
        for i, q in enumerate(questions, 1):
            print(f"\n--- Question {i} ---")
            print(f"Grade: {q.grade_level}")
            print(f"Topic: {q.topic}")
            print(f"Complexity: {q.complexity}")
            print(f"Question: {q.question_text}")
            print(f"Answer: {q.correct_answer}")
            print(f"Explanation: {q.explanation}")
    else:
        print("No questions generated - check the debug output above for issues")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate math questions using LLM')
    parser.add_argument('--grade', type=int, required=True, choices=range(1, 13), 
                        help='Grade level (1-12)')
    parser.add_argument('--topic', type=str, required=True, 
                        help='Math topic (e.g., Addition, Algebra, Calculus)')
    parser.add_argument('--complexity', type=str, required=True, 
                        choices=['easy', 'medium', 'hard'], 
                        help='Question complexity')
    parser.add_argument('--count', type=int, default=5, 
                        help='Number of questions to generate (default: 5)')
    parser.add_argument('--provider', type=str, default='ollama', 
                        choices=['ollama', 'openai'], 
                        help='LLM provider to use (default: ollama)')
    parser.add_argument('--save', action='store_true', 
                        help='Save questions to database')
    
    args = parser.parse_args()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    generator = LLMQuestionGenerator()
    
    print(f"Generating {args.count} {args.complexity} questions for Grade {args.grade} on {args.topic}...")
    
    questions = generator.generate_questions(
        grade_level=args.grade,
        topic=args.topic,
        complexity=args.complexity,
        count=args.count,
        provider=args.provider
    )
    
    if questions:
        print(f"\nGenerated {len(questions)} questions:")
        print("="*60)
        
        for i, question in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(f"Topic: {question.topic}")
            print(f"Question: {question.question_text}")
            print(f"Answer: {question.correct_answer}")
            print(f"Explanation: {question.explanation}")
            print("-" * 40)
        
        if args.save:
            if questions:
                save_questions_to_database(questions)
            else:
                print("ERROR: No questions were parsed successfully, cannot save to database.")
                print("This usually means the LLM output format doesn't match the expected parsing patterns.")
                print("Try using the debug mode: python question_generator.py debug")
    else:
        print("ERROR: No questions were generated. Please check your configuration and try again.")
        print("Common issues:")
        print("- Ollama service not running (if using ollama provider)")
        print("- Invalid API key (if using openai provider)")  
        print("- Network connectivity issues")
        print("- Model not available")
        print("\nTry using debug mode: python question_generator.py debug")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug_generation()
    else:
        main()
