import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.update(
        # Security
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev-key-123',
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        
        # Database
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
                             f'sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), "taskflow.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=os.environ.get('SQLALCHEMY_ECHO', 'false').lower() == 'true',
        
        # Session
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        
        # Uploads
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max upload
    )
    
    # Override with config file if provided
    if config is not None:
        app.config.update(config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app
