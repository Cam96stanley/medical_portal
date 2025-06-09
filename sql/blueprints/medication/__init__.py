from flask import Blueprint

medication_bp = Blueprint("medication_bp", __name__)

from . import routes