from flask_restx import Api
from flask import Blueprint

# Create main API blueprint
api_blueprint = Blueprint('api_v2', __name__)

# Initialize Flask-RESTX API
api = Api(
    api_blueprint,
    version='1.0',
    title='Mathopedia API',
    description='A comprehensive math learning platform API',
    doc='/docs/',  # Documentation will be available at /api/docs/
    validate=True,
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add a JWT token to the header with "Bearer " prefix'
        }
    },
    security='Bearer'
)

def init_api():
    """Initialize API namespaces"""
    # Import namespaces here to avoid circular imports
    from app.api.auth import api as auth_ns
    from app.api.questions import api as questions_ns
    from app.api.answers import api as answers_ns
    from app.api.profile import api as profile_ns
    from app.api.admin import api as admin_ns

    # Add namespaces
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(questions_ns, path='/questions')
    api.add_namespace(answers_ns, path='/answers')
    api.add_namespace(profile_ns, path='/profile')
    api.add_namespace(admin_ns, path='/admin')
