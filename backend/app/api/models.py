from flask_restx import fields
from app.api import api

# Common models
user_model = api.model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Account creation date')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email address', example='user@example.com'),
    'password': fields.String(required=True, description='Password', example='password123')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name', example='John'),
    'last_name': fields.String(required=True, description='Last name', example='Doe'),
    'email': fields.String(required=True, description='Email address', example='john.doe@example.com'),
    'password': fields.String(required=True, description='Password', example='password123')
})

token_response_model = api.model('TokenResponse', {
    'access_token': fields.String(required=True, description='JWT access token'),
    'user': fields.Nested(user_model, description='User information')
})

# Question models
question_model = api.model('Question', {
    'id': fields.Integer(required=True, description='Question ID'),
    'grade_level': fields.String(required=True, description='Grade level (1-12 or "Competitive Exams")'),
    'complexity': fields.String(required=True, description='Difficulty level', enum=['easy', 'medium', 'hard']),
    'topic': fields.String(required=True, description='Question topic'),
    'topic_id': fields.Integer(description='Topic reference ID'),
    'question_text': fields.String(required=True, description='Question text'),
    'correct_answer': fields.String(required=True, description='Correct answer'),
    'explanation': fields.String(required=True, description='Answer explanation'),
    'created_at': fields.DateTime(description='Question creation date')
})

question_request_model = api.model('QuestionRequest', {
    'grade_level': fields.String(description='Grade level filter'),
    'complexity': fields.String(description='Complexity filter', enum=['easy', 'medium', 'hard']),
    'topic': fields.String(description='Topic filter'),
    'limit': fields.Integer(description='Number of questions to return', default=10)
})

# Answer models
user_answer_model = api.model('UserAnswer', {
    'id': fields.Integer(required=True, description='Answer ID'),
    'user_id': fields.Integer(required=True, description='User ID'),
    'question_id': fields.Integer(required=True, description='Question ID'),
    'user_answer': fields.String(required=True, description='User\'s answer'),
    'is_correct': fields.Boolean(required=True, description='Whether answer is correct'),
    'answered_at': fields.DateTime(description='When answer was submitted'),
    'question': fields.Nested(question_model, description='Question details')
})

submit_answer_model = api.model('SubmitAnswer', {
    'question_id': fields.Integer(required=True, description='Question ID'),
    'user_answer': fields.String(required=True, description='User\'s answer')
})

answer_response_model = api.model('AnswerResponse', {
    'is_correct': fields.Boolean(required=True, description='Whether answer is correct'),
    'correct_answer': fields.String(required=True, description='The correct answer'),
    'explanation': fields.String(required=True, description='Answer explanation'),
    'user_answer': fields.String(required=True, description='User\'s submitted answer')
})

# Profile models
daily_progress_model = api.model('DailyProgress', {
    'id': fields.Integer(description='Progress ID'),
    'user_id': fields.Integer(description='User ID'),
    'date': fields.Date(required=True, description='Progress date'),
    'questions_answered': fields.Integer(description='Questions answered on this date'),
    'correct_answers': fields.Integer(description='Correct answers on this date'),
    'accuracy': fields.Float(description='Accuracy percentage for this date'),
    'total_time_spent': fields.Integer(description='Time spent in minutes')
})

grade_performance_model = api.model('GradePerformance', {
    'grade_level': fields.String(required=True, description='Grade level'),
    'grade_display': fields.String(required=True, description='Formatted grade display'),
    'total_questions': fields.Integer(required=True, description='Total questions attempted'),
    'correct_answers': fields.Integer(required=True, description='Correct answers'),
    'accuracy': fields.Float(required=True, description='Accuracy percentage')
})

topic_performance_model = api.model('TopicPerformance', {
    'topic_id': fields.Integer(required=True, description='Topic ID'),
    'topic_name': fields.String(required=True, description='Topic name'),
    'skill': fields.String(required=True, description='Skill description'),
    'total_questions': fields.Integer(required=True, description='Total questions attempted'),
    'correct_answers': fields.Integer(required=True, description='Correct answers'),
    'accuracy': fields.Float(required=True, description='Accuracy percentage')
})

topic_breakdown_model = api.model('TopicBreakdown', {
    'grade_level': fields.String(required=True, description='Grade level'),
    'grade_display': fields.String(required=True, description='Formatted grade display'),
    'total_topics': fields.Integer(required=True, description='Total topics in grade'),
    'topics_attempted': fields.Integer(required=True, description='Topics with attempted questions'),
    'topic_performance': fields.List(fields.Nested(topic_performance_model), description='Performance by topic')
})

stats_model = api.model('Stats', {
    'total_questions_answered': fields.Integer(description='Total questions answered'),
    'correct_answers': fields.Integer(description='Total correct answers'),
    'overall_accuracy': fields.Float(description='Overall accuracy percentage'),
    'current_streak': fields.Integer(description='Current study streak in days'),
    'total_study_days': fields.Integer(description='Total days with activity')
})

profile_response_model = api.model('ProfileResponse', {
    'id': fields.Integer(required=True, description='User ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Account creation date'),
    'stats': fields.Nested(stats_model, description='User statistics'),
    'daily_progress': fields.List(fields.Nested(daily_progress_model), description='Daily progress data'),
    'grade_performance': fields.List(fields.Nested(grade_performance_model), description='Grade-wise performance')
})

# Achievement models
achievement_model = api.model('Achievement', {
    'title': fields.String(required=True, description='Achievement title'),
    'description': fields.String(required=True, description='Achievement description'),
    'type': fields.String(required=True, description='Achievement type'),
    'earned': fields.Boolean(required=True, description='Whether achievement is earned')
})

achievements_response_model = api.model('AchievementsResponse', {
    'achievements': fields.List(fields.Nested(achievement_model), description='List of achievements'),
    'stats': fields.Nested(stats_model, description='User statistics')
})

# Topic model
topic_model = api.model('Topic', {
    'id': fields.Integer(required=True, description='Topic ID'),
    'topic': fields.String(required=True, description='Topic name'),
    'skill': fields.String(required=True, description='Skill description'),
    'grade_level': fields.String(required=True, description='Grade level'),
    'created_at': fields.DateTime(description='Topic creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

# Error models
error_model = api.model('Error', {
    'error': fields.String(required=True, description='Error message')
})

validation_error_model = api.model('ValidationError', {
    'message': fields.String(required=True, description='Validation error message'),
    'errors': fields.Raw(description='Field-specific validation errors')
})
