from flask import Blueprint

diagnoses_bp = Blueprint("diagnoses_bp", __name__)

from . import routes