from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import func
from sql.blueprints.diagnosis import diagnoses_bp
from sql.models import UserRole, db, Diagnosis, User
from sql.blueprints.diagnosis.schemas import diagnosis_schema
from sql.blueprints.user.schemas import return_users_schema
from sql.utils.auth import role_required

@diagnoses_bp.route("/<int:patient_id>", methods=["POST"])
@role_required(UserRole.DOCTOR)
def create_diagnosis(patient_id, user_id):
  doctor_id = user_id
  data = request.get_json()
  
  try:
    validated_data = diagnosis_schema.load(data)
    
  except ValidationError as e:
    return jsonify({
      "message": "Validation error",
      "errors": e.messages
      }), 400
  
  patient = User.query.get(patient_id)
  if not patient:
    return jsonify({
      "message": "Patient not found"
      }), 404
  
  
  existing = Diagnosis.query.filter_by(
    diagnosis_name=validated_data.diagnosis_name,
    patient_id=patient_id,
    doctor_id=doctor_id
  ).first()
  
  if existing:
    return jsonify({
      "message": "This diagnosis already exists for this patient"
      }), 409
  
  diagnosis = validated_data
  diagnosis.patient_id = patient_id
  diagnosis.doctor_id = doctor_id
  
  db.session.add(diagnosis)
  db.session.commit()
  
  return jsonify(diagnosis_schema.dump(diagnosis)), 201

@diagnoses_bp.route("/patients/<diagnosis_name>", methods=["GET"])
@role_required(UserRole.DOCTOR)
def get_patients_with_diagnosis(diagnosis_name, user_id):
  diagnoses = Diagnosis.query.filter(func.lower(Diagnosis.diagnosis_name) == diagnosis_name.lower(), Diagnosis.doctor_id == user_id).all()
  
  if not diagnoses:
    return jsonify({"message": "No patients found with this diagnosis"}), 404
  
  patients = [diagnosis.patient for diagnosis in diagnoses if diagnosis.patient and diagnosis.patient.is_active]
  unique_patients = list({p.id: p for p in patients}.values())
  
  if not unique_patients:
    return jsonify({"message": "No patients found"}), 404
  
  return jsonify(return_users_schema.dump(unique_patients)), 200