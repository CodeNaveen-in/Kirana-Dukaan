import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'
    # Add other universal settings here

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    # In production, you'd use a real DB like PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')