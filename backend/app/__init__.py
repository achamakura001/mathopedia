from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()



def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS with proper settings
    CORS(app, 
         origins=app.config.get('CORS_ORIGINS', ['*']),
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Register original blueprints for backward compatibility
    from app.routes.auth import auth_bp
    from app.routes.questions import questions_bp
    from app.routes.answers import answers_bp
    from app.routes.profile import profile_bp
    from app.routes.admin import admin_bp
    from app.routes.analytics import analytics_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(answers_bp, url_prefix='/api/answers')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    # Register new Flask-RESTX API
    from app.api import api_blueprint, init_api
    init_api()  # Initialize the API namespaces
    app.register_blueprint(api_blueprint, url_prefix='/api/v2')
    
    # Add a simple health check endpoint for CORS testing
    @app.route('/api/health', methods=['GET', 'OPTIONS'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'API is running',
            'cors_origins': app.config.get('CORS_ORIGINS', []),
            'swagger_docs': '/api/v2/docs/'
        })
    
    return app
