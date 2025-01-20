"""
This module loads environment variables and defines the configuration 
class for the Flask application.
"""

import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables from a .env file if it exists
ENV = find_dotenv('.env')
if ENV:
    load_dotenv(ENV)

class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        APP_SECRET_KEY (str): The secret key for the application.
        SQLALCHEMY_DATABASE_URI (str): The database URI for SQLAlchemy.
    """
    APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 
        'postgresql://postgres:postgres@localhost:5432/postgres')
