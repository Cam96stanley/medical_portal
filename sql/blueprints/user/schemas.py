from marshmallow import fields, validates_schema, ValidationError
from sql.extensions import ma
from sql.models import User, EnumField, UserRole

class UserSchema(ma.SQLAlchemyAutoSchema):
  dob = fields.Date(allow_none=True)
  
  role = EnumField(UserRole, required=True)
  class Meta:
    model = User
    load_instance = True
    include_fk = True
    
  password = fields.String(load_only=True, required=True)
    
  @validates_schema
  def validate_dob_for_patients(self, data, **kwargs):
    if data.get("role") == UserRole.PATIENT and not data.get("dob"):
      raise ValidationError("Date of birth is required for patients.", field_name="dob")

user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password",))
return_users_schema = UserSchema(many=True, exclude=("password",))