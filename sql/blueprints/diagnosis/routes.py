from flask import jsonify
from sql.blueprints.diagnosis import diagnosis_bp
from sql.models import Diagnosis
from sql.blueprints.diagnosis.schemas import diagnoses_schema
from sql.utils.auth import token_required

@diagnosis_bp.route("/patients/<diagnosis_name>", methods=["GET"])
def get_patients_with_diagnosis(diagnosis_name, _user_id):
  diagnoses = Diagnosis.query.filter_by(diagnosis_name=diagnosis_name).all()
  return jsonify(diagnoses_schema.dump(diagnoses)), 200