from flask import request, jsonify
from marshmallow import ValidationError
from sql.models import BloodPressure, HeartRate, Weight, Glucose, Temperature, User, db
from sql.blueprints.vitals.schemas import bloodpressure_schema, heartrate_schema, weight_schema, glucose_schema, temperature_schema
from sql.blueprints.vitals import blood_pressure_bp, heart_rate_bp, weight_bp, glucose_bp, temperature_bp
from sql.utils.auth import token_required

@blood_pressure_bp.route("/<int:patient_id>", methods=["POST"])
@token_required
def create_bp_entry(patient_id):
  json_data = request.get_json()
  if not json_data:
    return json_data({"message": "No input data"}), 400
  
  try:
    bp_entry: BloodPressure = bloodpressure_schema.load(json_data)
  except ValidationError as e:
    return json_data({"message": e.messages}), 400
  
  patient = db.session.get(User, patient_id)
  if not patient:
    return jsonify({"message": f"Patient with ID {patient_id} not found"}), 404
  
  bp_entry.patient_id = patient_id
  db.session.add(bp_entry)
  
  try:
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": str(e)}), 500
  
  return bloodpressure_schema.jsonify(bp_entry), 201