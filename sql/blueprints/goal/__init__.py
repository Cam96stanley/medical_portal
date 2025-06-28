from flask import Blueprint

goal_bp = Blueprint("goal_bp", __name__)

from . import routes