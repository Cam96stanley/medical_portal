from flask import Flask
from sql.models import db
from sql.extensions import ma
from sql.blueprints.user import user_bp
from sql.blueprints.diagnosis import diagnosis_bp

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  
  db.init_app(app)
  ma.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(diagnosis_bp, url_prefix="/diagnoses")
  
  return app