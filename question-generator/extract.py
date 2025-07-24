import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class QuestionData:
    grade_level: int
    complexity: str
    topic: str
    question_text: str
    correct_answer: str
    explanation: str


def parse_answer(answer_text):
    """
    Parse the answer field to extract detailed solution and final answer.
    
    Args:
        answer_text (str): The complete answer text from the JSONL
        
    Returns:
        tuple: (detailed_solution, final_answer)
    """
    # Split by the final answer marker "####"
    parts = answer_text.split('####')
    
    if len(parts) != 2:
        raise ValueError(f"Invalid answer format - expected '####' separator: {answer_text}")
    
    detailed_solution = parts[0].strip()
    final_answer = parts[1].strip()
    
    # Validate that final answer is numeric
    try:
        # Handle commas in numbers and convert to int/float
        numeric_answer = final_answer.replace(',', '')
        if '.' in numeric_answer:
            float(numeric_answer)
        else:
            int(numeric_answer)
    except ValueError:
        raise ValueError(f"Final answer is not numeric: {final_answer}")
    
    detailed_solution = re.sub(r'<<[^>]*>>', ' ', detailed_solution)  # Remove placeholders
    detailed_solution = re.sub(r'\s+', ' ', detailed_solution)  # Normalize whitespace
    detailed_solution = detailed_solution.strip()  # Trim leading/trailing whitespace

    return detailed_solution, final_answer

def process_jsonl_file(input_file, output_file):
    """
    Process the JSONL file and create separated output.
    
    Args:
        input_file (str): Path to input JSONL file
        output_file (str): Path to output file
    """
    processed_data = []
    questions = []
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Parse JSON line
                    data = json.loads(line)
                    
                    # Validate required fields
                    if 'question' not in data or 'answer' not in data:
                        print(f"Warning: Line {line_num} missing required fields, skipping")
                        continue
                    
                    question = data['question']
                    answer_text = data['answer']
                    
                    # Parse the answer into solution and final answer
                    detailed_solution, final_answer = parse_answer(answer_text)
                    
                    # Create structured output
                    processed_item = {
                        'question': question,
                        'detailed_solution': detailed_solution,
                        'final_answer': final_answer
                    }
                    questions.append(QuestionData(
                        grade_level="Competitive Exams",
                        complexity="medium",
                        topic="Word Problems",
                        question_text=question,
                        correct_answer=final_answer,
                        explanation=detailed_solution
                    ))
                    
                    processed_data.append(processed_item)
                    
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON on line {line_num}: {e}")
                    continue
                except ValueError as e:
                    print(f"Warning: Line {line_num} - {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line {line_num}: {e}")
                    continue
        # Save questions to database
        save_questions_to_database(questions)

        # Write processed data to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in processed_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"Successfully processed {len(processed_data)} items")
        print(f"Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def save_questions_to_database(questions: List[QuestionData]):
    """Save generated questions to the database"""
    
    # Add the backend path to sys.path
    import sys
    from pathlib import Path
    backend_path = Path(__file__).parent.parent / "backend"
    sys.path.append(str(backend_path))
    
    # Import here to avoid circular imports
    from app import create_app, db
    from app.models import Question
    
    app = create_app()
    
    with app.app_context():
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
                    question_text=question_data.question_text,
                    correct_answer=question_data.correct_answer,
                    explanation=question_data.explanation
                )
                db.session.add(question)
                saved_count += 1
        
        try:
            db.session.commit()
            print(f"Successfully saved {saved_count} new questions to database!")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving questions to database: {e}")
            raise

def main():
    """Main function to run the data separator script."""
    
    # Set up file paths
    input_file = "data.jsonl"
    output_file = "separated_data.jsonl"
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found in current directory")
        sys.exit(1)
    
    print(f"Processing file: {input_file}")
    process_jsonl_file(input_file, output_file)

if __name__ == "__main__":
    main()