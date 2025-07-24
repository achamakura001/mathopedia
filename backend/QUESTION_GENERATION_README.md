# Question Generation Feature

## Overview
The admin panel now includes the ability to generate new math questions for any topic and grade level using AI/LLM services.

## Features

### Admin Panel Integration
- **Generate Questions Button**: Each topic in the admin panel has a generate button (✨ icon)
- **Question Statistics**: Shows current question counts by complexity (Easy, Medium, Hard)
- **Real-time Updates**: Question counts update immediately after generation

### Generation Options
- **Complexity Levels**: Easy, Medium, Hard
- **Question Count**: 1-20 questions per generation
- **Provider Selection**: Ollama (local) or OpenAI (cloud)
- **Topic-specific**: Uses topic name and skill description for context

## How It Works

### 1. Backend API
- **Endpoint**: `POST /api/admin/generate-questions`
- **Requires**: Admin authentication
- **Parameters**:
  ```json
  {
    "topic_id": 2,
    "complexity": "medium", 
    "count": 5,
    "provider": "ollama"
  }
  ```

### 2. Question Generation Service
- **Primary**: Uses real LLM providers (Ollama/OpenAI) with customizable prompts
- **Fallback**: Mock generator for testing/demo when LLM services unavailable
- **Prompt Template**: Located in `/common/question_generation_prompt.txt`

### 3. Database Integration
- **Automatic Saving**: Generated questions saved to database
- **Topic Linking**: Questions linked to topics via foreign key
- **Duplicate Prevention**: Checks for existing questions before saving

## File Structure

```
/backend/
  /app/routes/admin.py          - Admin API endpoints
  question_generator_service.py - Real LLM service integration
  mock_question_generator.py    - Testing/demo fallback

/question-generator/
  question_generator.py         - Core LLM question generation

/common/
  question_generation_prompt.txt - Customizable prompt template

/frontend/src/pages/
  AdminPanel.js                 - UI for question generation
```

## Setup for Production

### 1. Ollama (Local LLM)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a math-focused model
ollama pull qwen2-math

# Set environment variables
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=qwen2-math
```

### 2. OpenAI (Cloud)
```bash
# Set API key
export OPENAI_API_KEY=your_api_key_here
```

### 3. Dependencies
```bash
# Backend dependencies
pip install requests python-dotenv

# Ensure all Flask dependencies are installed
pip install -r requirements.txt
```

## Usage

### Admin Interface
1. Login as admin user
2. Navigate to Admin Panel
3. Find the topic you want to generate questions for
4. Click the ✨ (generate) button
5. Select:
   - **Provider**: Ollama or OpenAI
   - **Complexity**: Easy, Medium, or Hard
   - **Count**: Number of questions (1-20)
6. Click "Generate Questions"
7. Wait for generation to complete
8. Question counts will update automatically

### Command Line (Development)
```bash
# Using the enhanced service
cd backend
python question_generator_service.py --topic-id 2 --complexity medium --count 5

# Using the original generator
cd question-generator
python question_generator.py --grade 4 --topic "Fractions" --complexity medium --count 5 --save
```

## Prompt Customization

Edit `/common/question_generation_prompt.txt` to customize how questions are generated:

- **Context Variables**: `{count}`, `{grade_level}`, `{topic}`, `{complexity}`, `{skill_description}`
- **Guidelines**: Modify complexity rules and question types
- **Format**: Adjust question/answer/explanation structure

## Error Handling

- **LLM Service Unavailable**: Automatically falls back to mock generator
- **Invalid Parameters**: Returns validation errors
- **Database Errors**: Handles duplicates and transaction rollbacks
- **Network Issues**: Graceful timeout and retry logic

## Security

- **Admin Only**: All generation endpoints require admin authentication
- **Input Validation**: Parameters validated for type and range
- **Rate Limiting**: Prevent abuse of LLM services (implement as needed)

## Monitoring

- **Success Metrics**: Track questions generated vs saved
- **Error Logging**: LLM service failures and database issues
- **Usage Stats**: Monitor generation frequency by topic/complexity

## Future Enhancements

- **Batch Generation**: Generate for multiple topics at once
- **Quality Scoring**: Rate generated questions for difficulty/appropriateness
- **Template Management**: Multiple prompt templates for different question types
- **Review System**: Admin review before questions go live
- **Export/Import**: Bulk question management
