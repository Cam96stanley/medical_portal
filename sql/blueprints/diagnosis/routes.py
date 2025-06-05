from flask import jsonify, request
from marshmallow import ValidationError
from sql.blueprints.diagnosis import diagnoses_bp
from sql.models import db, Diagnosis, User
from sql.blueprints.diagnosis.schemas import diagnosis_schema, diagnoses_schema
from sql.utils.auth import doctor_required

@diagnoses_bp.route("/<int:patient_id>", methods=["POST"])
@doctor_required
def create_diagnosis(patient_id, doctor_id):
  data = request.get_json()
  
  try:
    validated_data = diagnosis_schema.load(data)
  except ValidationError as err:
    return jsonify({"errors": err.messages}), 400
  
  patient = User.query.get(patient_id)
  if not patient:
    return jsonify({"message": "Patient not found"}), 404
  
  
  existing = Diagnosis.query.filter_by(
    diagnosis_name=validated_data.diagnosis_name,
    patient_id=patient_id,
    doctor_id=doctor_id
  ).first()
  
  if existing:
    return jsonify({"message": "This diagnosis already exists for this patient"}), 409
  
  diagnosis = validated_data
  diagnosis.patient_id = patient_id
  diagnosis.doctor_id = doctor_id
  
  db.session.add(diagnosis)
  db.session.commit()
  
  return jsonify(diagnosis_schema.dump(diagnosis)), 201

@diagnoses_bp.route("/patients/<diagnosis_name>", methods=["GET"])
@doctor_required
def get_patients_with_diagnosis(diagnosis_name, _doctor_id):
  diagnoses = Diagnosis.query.filter_by(diagnosis_name=diagnosis_name).all()
  return jsonify(diagnoses_schema.dump(diagnoses)), 200