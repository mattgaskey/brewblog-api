from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import environ as env
from dotenv import find_dotenv, load_dotenv
from flask_cors import CORS
from config import Config

ENV = find_dotenv('.env')
if ENV:
  load_dotenv(ENV)

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)
  app.secret_key = env.get("APP_SECRET_KEY")

  db.init_app(app)
  migrate.init_app(app, db)

  CORS(app, origins="*", supports_credentials=True)

  from brewblog.beer import bp as beer_bp
  app.register_blueprint(beer_bp)

  from brewblog.brewery import bp as brewery_bp
  app.register_blueprint(brewery_bp)

  return app

from brewblog import models