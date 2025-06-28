from flask import Flask
from sql.models import db
from sql.extensions import ma, migrate
from sql.blueprints.user import user_bp
from sql.blueprints.diagnosis import diagnoses_bp
from sql.blueprints.medication import medication_bp
from sql.blueprints.goal import goal_bp
from sql.blueprints.vitals import blood_pressure_bp, heart_rate_bp, weight_bp, glucose_bp, temperature_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config = {
    "app_name": "Health Portal"
  }
)

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  
  db.init_app(app)
  ma.init_app(app)
  migrate.init_app(app, db)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(diagnoses_bp, url_prefix="/diagnoses")
  app.register_blueprint(medication_bp, url_prefix="/medications")
  app.register_blueprint(goal_bp, url_prefix="/goals")
  app.register_blueprint(blood_pressure_bp, url_prefix="/bp")
  app.register_blueprint(heart_rate_bp, url_prefix="/heartrate")
  app.register_blueprint(weight_bp, url_prefix="weight")
  app.register_blueprint(glucose_bp, url_prefix="glucose")
  app.register_blueprint(temperature_bp, url_prefix="temperature")
  app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
  
  return app