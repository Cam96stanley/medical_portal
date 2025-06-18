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
  try:
    patient = User.query.get(patient_id)
    if not patient or patient.role != UserRole.PATIENT:
      return jsonify({"message": "Patient not found"}), 404
    
    medications = Medication.query.filter_by(patient_id=patient_id).all()
    
    if not medications:
      return jsonify({"message": "No medications found for this patient"}), 200
    
    return jsonify(medications_schema.dump(medications)), 200
  
  except Exception as e:
    return jsonify({
      "message": "Internal server error",
      "details": str(e)
      }), 500
    
@medication_bp.route("/patients/<int:patient_id>/medications/<int:medication_id>/deactivate", methods=["PATCH"])
@role_required(UserRole.DOCTOR)
def deactivate_medication(patient_id, medication_id, user_id):
  data = request.get_json()
  reason = data.get("deactivation_reason", "").strip()
  
  if not reason:
    return jsonify({"message": "Deactivation reason is required"}), 400
  
  patient = User.query.get(patient_id)
  if not patient or patient.role != UserRole.PATIENT:
    return jsonify({"message": "Patient not found"}), 404
  
  medication = Medication.query.filter_by(id=medication_id, patient_id=patient_id).first()
  if not medication:
    return jsonify({"message": "Medication not found"}), 404
  
  if not medication.active:
    return jsonify({"message": "Medication is already inactive"}), 400
  
  try:
    medication.active = False
    medication.deactivation_reason = reason
    db.session.commit()
    return jsonify({
      "message": "Mediaction successfully deactivated"
      }), 200
  
  except Exception as e:
    return jsonify({
      "message": "Failed to deactivate medication",
      "details": str(e)
    }), 500