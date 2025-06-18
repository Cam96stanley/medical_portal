from flask import jsonify, request
from marshmallow import ValidationError
from sql.models import Medication, User, UserRole, db
from sql.blueprints.medication import medication_bp
from sql.blueprints.medication.schemas import medication_schema, medications_schema
from sql.utils.auth import role_required

@medication_bp.route("/<int:patient_id>", methods=["POST"])
@role_required(UserRole.DOCTOR)
def create_medication(patient_id, user_id):
  data = request.get_json()
  
  if not data:
    return jsonify({"message": "No input data provided"}), 400
  
  patient = User.query.get(patient_id)
  if not patient or patient.role != UserRole.PATIENT:
    return jsonify({"message": "Patient not found"}), 404
  
  try:
    new_medication = medication_schema.load(data)
    new_medication.patient_id = patient_id
    db.session.add(new_medication)
    db.session.commit()
    return jsonify(medication_schema.dump(new_medication)), 201
  
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  
  except Exception as e:
      db.session.rollback()
      return jsonify({
        "message": "Internal server error",
        "details": str(e)
        }), 500

@medication_bp.route("/patients/<int:patient_id>", methods=["GET"])
@role_required(UserRole.DOCTOR)
def get_meds_for_user(patient_id, user_id):
  patient = User.query.get(patient_id)
  if not patient or patient.role != UserRole.PATIENT:
    return jsonify({"message": "Patient not found"}), 404
  
  medications = Medication.query.filter_by(patient_id=patient_id).all()
  
  return jsonify(medications_schema.dump(medications)), 200