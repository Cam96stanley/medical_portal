from flask import Blueprint

blood_pressure_bp = Blueprint("blood_pressure_bp", __name__)
heart_rate_bp = Blueprint("heart_rate_bp", __name__)
weight_bp = Blueprint("weight_bp", __name__)
glucose_bp = Blueprint("glucose_bp", __name__)
temperature_bp = Blueprint("temperature_bp", __name__)

from . import routes