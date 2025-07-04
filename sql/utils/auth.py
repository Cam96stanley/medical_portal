from flask_bcrypt import Bcrypt
from functools import wraps
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, jsonify, request
import jose

bcrypt = Bcrypt()

def hash_password(plain_password: str) -> str:
  return bcrypt.generate_password_hash(plain_password).decode("utf-8")

def check_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.check_password_hash(hashed_password, plain_password)

def generate_token(user):
  payload = {
    "sub": str(user.id),
    "role": user.role.value,
    "exp": datetime.now(timezone.utc) + timedelta(days=1)
  }
  
  token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
  return token

def role_required(*allowed_roles):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      auth_header = request.headers.get("Authorization")
      if not auth_header:
        return jsonify({"message": "Missing token"}), 401
      
      try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        role = payload.get("role")
        if role not in [r.value for r in allowed_roles]:
          return jsonify({"message": f"{' or '.join(r.value for r in allowed_roles)} role required"}), 403
        user_id = payload.get("sub")
      except jose.exceptions.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
      except JWTError:
        return jsonify({"message": "Invalid token"}), 401
      
      return f(*args, user_id=user_id, **kwargs)
    return wrapper
  return decorator

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    
    if "Authorization" in request.headers:
      auth_header = request.headers["Authorization"]
      parts = auth_header.split(" ")
      if len(parts) == 2 and parts[0] == "Bearer":
        token = parts[1]
      
    if not token:
      return jsonify({"message": "Token is missing"}), 401
    
    try:
      data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
      user_id = data["sub"]
      role = data.get("role")
      
    except jose.exceptions.ExpiredSignatureError:
      return jsonify({"message": "Token has expired!"}), 401
    
    except jose.exceptions.JWTError:
      return jsonify({"message": "Invalid token!"}), 401
    
    return f(*args, **kwargs)
  return decorated