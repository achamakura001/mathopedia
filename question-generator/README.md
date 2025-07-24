# Question Generator Setup Guide

## Overview

The Question Generator is a utility that uses Large Language Models (LLMs) to automatically generate math questions for different grade levels, topics, and complexity levels.

## Supported LLM Providers

- **Ollama** (Local LLM - Default)
- **OpenAI GPT** (Cloud API)
- **Anthropic Claude** (Cloud API - Future)

## Prerequisites

### For Ollama (Local)
1. **Install Ollama:**
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Pull a model:**
   ```bash
   ollama pull llama2
   # or
   ollama pull codellama
   # or
   ollama pull mistral
   ```

### For OpenAI
1. Get an API key from [OpenAI](https://platform.openai.com/)
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

## Installation

1. **Navigate to the question-generator directory:**
   ```bash
   cd question-generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp ../.env.example .env
   ```
   
   Edit `.env`:
   ```env
   # Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   
   # OpenAI Configuration (optional)
   OPENAI_API_KEY=your-openai-api-key
   
   # Database Configuration (if saving to database)
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your-password
   MYSQL_DB=mathopedia
   ```

## Usage

### Command Line Interface

```bash
python question_generator.py [OPTIONS]
```

#### Options:
- `--grade` (required): Grade level (1-12)
- `--topic` (required): Math topic (e.g., "Addition", "Algebra", "Calculus")
- `--complexity` (required): Question complexity (easy, medium, hard)
- `--count`: Number of questions to generate (default: 5)
- `--provider`: LLM provider (ollama, openai) (default: ollama)
- `--save`: Save questions to database

#### Examples:

**Generate 5 easy addition questions for Grade 1:**
```bash
python question_generator.py --grade 1 --topic "Addition" --complexity easy --count 5
```

**Generate and save 10 medium algebra questions for Grade 8:**
```bash
python question_generator.py --grade 8 --topic "Algebra" --complexity medium --count 10 --save
```

**Use OpenAI instead of Ollama:**
```bash
python question_generator.py --grade 10 --topic "Trigonometry" --complexity hard --provider openai --save
```

### Batch Generation

Create a script to generate questions for multiple grades/topics:

```bash
#!/bin/bash

# Generate questions for different grades and topics
python question_generator.py --grade 1 --topic "Addition" --complexity easy --count 20 --save
python question_generator.py --grade 1 --topic "Subtraction" --complexity easy --count 20 --save
python question_generator.py --grade 2 --topic "Multiplication" --complexity easy --count 15 --save
python question_generator.py --grade 3 --topic "Division" --complexity medium --count 15 --save
# ... add more as needed
```

### Python API Usage

```python
from question_generator import LLMQuestionGenerator, save_questions_to_database

# Initialize generator
generator = LLMQuestionGenerator()

# Generate questions
questions = generator.generate_questions(
    grade_level=5,
    topic="Fractions",
    complexity="medium",
    count=10,
    provider="ollama"
)

# Print questions
for question in questions:
    print(f"Q: {question.question_text}")
    print(f"A: {question.correct_answer}")
    print(f"Explanation: {question.explanation}")
    print("-" * 50)

# Save to database
save_questions_to_database(questions)
```

## Topics by Grade Level

### Elementary (Grades 1-5)
- Addition, Subtraction
- Multiplication, Division
- Fractions, Decimals
- Basic Geometry
- Word Problems

### Middle School (Grades 6-8)
- Ratios and Proportions
- Integers, Rational Numbers
- Basic Algebra
- Geometry and Measurement
- Statistics and Probability

### High School (Grades 9-12)
- Algebra I & II
- Geometry
- Trigonometry
- Pre-Calculus
- Calculus
- Statistics

## Question Quality Tips

1. **Be Specific with Topics:**
   - Instead of "Math", use "Linear Equations"
   - Instead of "Geometry", use "Area and Perimeter"

2. **Adjust Complexity:**
   - **Easy**: Basic computation, single-step problems
   - **Medium**: Multi-step problems, some reasoning
   - **Hard**: Complex problems, multiple concepts

3. **Review Generated Questions:**
   - Always review questions before adding to database
   - Check for mathematical accuracy
   - Ensure age-appropriate language

## Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve

# List available models
ollama list

# Pull a new model if needed
ollama pull llama2
```

### OpenAI Issues
- Verify API key is correct
- Check API usage limits
- Ensure sufficient credits

### Database Issues
- Verify database connection settings
- Ensure database and tables exist
- Check user permissions

## Performance Considerations

- **Ollama**: Slower but free, runs locally
- **OpenAI**: Faster but costs money, requires internet
- Generate questions in batches for efficiency
- Monitor token usage for cloud providers

## Future Enhancements

- Support for more LLM providers (Claude, Gemini)
- Image-based questions
- Interactive/dynamic questions
- Question difficulty auto-adjustment
- Multi-language support
