from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User
from app.api.models import login_model, register_model, token_response_model, user_model, error_model

api = Namespace('auth', description='Authentication operations')

@api.route('/login')
class LoginResource(Resource):
    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.marshal_with(token_response_model)
    @api.response(200, 'Login successful', token_response_model)
    @api.response(401, 'Invalid credentials', error_model)
    @api.response(400, 'Validation error', error_model)
    def post(self):
        """User login"""
        data = api.payload
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            api.abort(401, 'Invalid email or password')
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }

@api.route('/register')
class RegisterResource(Resource):
    @api.doc('user_register')
    @api.expect(register_model, validate=True)
    @api.marshal_with(token_response_model)
    @api.response(201, 'Registration successful', token_response_model)
    @api.response(400, 'Email already exists or validation error', error_model)
    def post(self):
        """User registration"""
        data = api.payload
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            api.abort(400, 'Email already registered')
        
        # Create new user
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            api.abort(400, f'Registration failed: {str(e)}')
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, 201

@api.route('/me')
class CurrentUserResource(Resource):
    @api.doc('get_current_user')
    @api.marshal_with(user_model)
    @api.response(200, 'Success', user_model)
    @api.response(401, 'Unauthorized', error_model)
    @api.response(404, 'User not found', error_model)
    @jwt_required()
    def get(self):
        """Get current user information"""
        current_user_id = get_jwt_identity()
        
        user = User.query.get(current_user_id)
        if not user:
            api.abort(404, 'User not found')
        
        return user.to_dict()
