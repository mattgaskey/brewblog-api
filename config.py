import os
from dotenv import find_dotenv, load_dotenv

ENV = find_dotenv('.env')
if ENV:
  load_dotenv(ENV)

class Config:
  APP_SECRET_KEY = os.environ.get('APP_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/postgres')

