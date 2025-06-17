from flask import jsonify, request
from marshmallow import ValidationError
from sql.models import UserRole, db
from sql.blueprints.medication import medication_bp
from sql.blueprints.medication.schemas import medication_schema
from sql.utils.auth import role_required

@medication_bp.route("/", methods=["POST"])
@role_required(UserRole.DOCTOR)
def create_medication():
  data = request.get_json()
  
  if not data:
    return jsonify({"message": "No input data provided"}), 400
  
  try:
    new_medication = medication_schema.load(data)
    db.session.add(new_medication)
    db.session.commit()
    return jsonify(medication_schema.dump(new_medication)), 201
  
  except ValidationError as e:
    return jsonify({"error": str(e)}), 400