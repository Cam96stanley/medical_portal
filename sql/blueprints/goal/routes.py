from datetime import datetime, timezone
from flask import jsonify, request
from marshmallow import ValidationError
from sql.blueprints.goal import goal_bp
from sql.models import db, Goal, UserRole, User
from sql.blueprints.goal.schemas import goal_schema
from sql.utils.auth import role_required

@goal_bp.route("/<int:patient_id>", methods=["POST"])
@role_required(UserRole.DOCTOR)
def create_goal(patient_id, user_id):
  json_data = request.get_json()
  
  if not json_data:
    return jsonify({"message": "No input data provided"}), 400
  
  try:
    validated_data = goal_schema.load(json_data)
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  
  patient = db.session.get(User, patient_id)
  if not patient:
    return jsonify({"message": f"Patient with ID {patient_id} does not exist"}), 404
  
  try:
    new_goal = Goal(
      patient_id=patient_id,
      created_by=user_id,
      title=validated_data["title"],
      description=validated_data["description"],
      target_date=validated_data["target_date"],
      is_complete=validated_data.get("is_complete", False),
      created_at=datetime.now(timezone.utc)
    )
    
    db.session.add(new_goal)
    db.session.commit()
    
    return goal_schema.jsonify(new_goal), 201
  
  except Exception as e:
    db.session.rollback()
    return jsonify({"message": str(e)}), 500