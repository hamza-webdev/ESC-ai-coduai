from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .models import db
import os

def create_app(config_object=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        app.config.from_pyfile('../config.py')
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    
    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create a simple route for testing
    @app.route('/')
    def index():
        return {'message': 'Welcome to Espoir Sportif de Chorbane API'}
    
    return app