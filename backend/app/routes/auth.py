from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from app import db
from app.models import User
from app.utils import get_current_user_id

auth_bp = Blueprint('auth', __name__)

class RegisterSchema(Schema):
    first_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    last_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

@auth_bp.route('/register', methods=['POST'])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        first_name=data['first_name'].strip(),
        last_name=data['last_name'].strip(),
        email=data['email'].lower().strip()
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'error': 'Validation error', 'messages': err.messages}), 400
    
    user = User.query.filter_by(email=data['email'].lower().strip()).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_current_user_id()
    
    if not current_user_id:
        return jsonify({'error': 'Invalid user authentication'}), 401
    
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200
