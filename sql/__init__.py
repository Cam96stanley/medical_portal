from flask import Flask
from sql.models import db
from sql.extensions import ma
from sql.blueprints.user import user_bp

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  
  db.init_app(app)
  ma.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  
  return app