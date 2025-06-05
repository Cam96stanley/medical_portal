from flask import Blueprint

diagnosis_bp = Blueprint("diagnosis_bp", __name__)

from . import routes