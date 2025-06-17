from marshmallow import fields, validates_schema, ValidationError
from sql.extensions import ma
from sql.models import User, EnumField, UserRole

class LowercaseEnumField(fields.Field):
  def __init__(self, enum, *args, **kwargs):
    self.enum = enum
    super().__init__(*args, **kwargs)
    
  def _deserialize(self, value, attr, data, **kwargs):
    try:
      return self.enum(value.lower())
    except ValueError:
      valid_values = [e.value for e in self.enum]
      raise ValidationError(
        f"Invalid value '{value}'. Must be one of: {valid_values}"
      )

  def _serialize(self, value, attr, obj, **kwargs):
    if isinstance(value, self.enum):
      return value.value
    return None

class UserSchema(ma.SQLAlchemyAutoSchema):
  dob = fields.Date(allow_none=True)
  role = LowercaseEnumField(UserRole, required=True)
  
  class Meta:
    model = User
    load_instance = True
    include_fk = True
    
  password = fields.String(load_only=True, required=True)
    
  @validates_schema
  def validate_dob_for_patients(self, data, **kwargs):
    if data.get("role") == UserRole.PATIENT and not data.get("dob"):
      raise ValidationError({"dob": "Date of birth is required for patients"})

user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password",))
return_users_schema = UserSchema(many=True, exclude=("password",))