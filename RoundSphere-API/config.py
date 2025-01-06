import os
from datetime import timedelta

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS settings - allow Django frontend
    CORS_ORIGINS = [
        'http://localhost:8000',  # Django development server
        'http://127.0.0.1:8000',
        os.environ.get('FRONTEND_URL', '')  # Production frontend URL
    ]
    
    # API settings
    API_TITLE = 'RoundSphere API'
    API_VERSION = '1.0'
    API_DESCRIPTION = 'API for managing products, orders, and payment operations'
    
    # Swagger settings
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_OPERATION_ID = True
