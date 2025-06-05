from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sql.models import db, User
from sql.blueprints.user import user_bp
from sql.blueprints.user.schemas import user_schema, return_user_schema, return_users_schema
from sql.utils.auth import hash_password, check_password, generate_token, token_required

@user_bp.route("/login", methods=["POST"])
def login_user():
  data = request.get_json()
  
  if not data or not data.get("email") or not data.get("password"):
    return jsonify({"error": "Email and password are required"}), 400
  
  user = db.session.query(User).filter_by(email=data["email"]).first()
  
  if not user or not check_password(data["password"], user.password):
    return jsonify({"error": "Invalid email or password"}), 401
  
  token = generate_token(user)
  
  return jsonify({
    "message": "User logged in successfully",
    "token": token,
    "user": {
      "id": user.id,
      "email": user.email,
      "role": user.role.value, 
      "name": user.name
    }
  }), 200


@user_bp.route("/", methods=["POST"])
def create_user():
    user_data = user_schema.load(request.json)
    user_data.password = hash_password(user_data.password)
    
    db.session.add(user_data)
    db.session.commit()
    
    return jsonify(return_user_schema.dump(user_data)), 201


@user_bp.route("/", methods=["GET"])
def get_users():
  query = db.session.query(User)
  users = db.session.execute(query).scalars().all()
  
  if not users:
    return jsonify({"message": "No users found"})
  
  return jsonify(return_users_schema.dump(users)), 200


@user_bp.route("/me", methods=["GET"])
@token_required
def get_user(user_id):
  query = db.session.query(User).where(User.id == user_id)
  user = db.session.execute(query).scalars().first()
  
  if user is None:
    return jsonify({"message": "No user found with that id"}), 404
  
  return jsonify(return_user_schema.dump(user)), 200


@user_bp.route("/me", methods=["PATCH"])
@token_required
def update_user(user_id):
  user = db.session.get(User, user_id)
  
  if not user:
    return jsonify({"error": "user not found"}), 404
  
  data = request.json
  
  try:
    
    updated_data = user_schema.load(data, partial=True)
    
    if "password" in data:
      user.password = hash_password(data["password"])
    
    for key, value in updated_data.items():
      if key != "password":
        setattr(user, key, value)
    
    db.session.commit()
    return jsonify(return_user_schema.dump(user)), 200

  except ValidationError as err:
    return jsonify(err.messages), 400
  except IntegrityError:
    db.session.rollback()
    return jsonify({"error": "Email already in use"}), 409
  except Exception:
    db.session.rollback()
    return jsonify({"error": "Database error"}), 500


@user_bp.route("/me", methods=["DELETE"])
@token_required
def delete_user(user_id):
  user = db.session.get(User, user_id)
  
  if not user:
    return jsonify({"message": "User not found"}), 404
  
  db.session.delete(user)
  db.session.commit()
  
  return jsonify({"message": f"User {user.id} deleted successfully"}), 200