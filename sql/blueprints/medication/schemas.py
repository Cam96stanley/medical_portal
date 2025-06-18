from marshmallow import ValidationError, validates_schema
from sql.extensions import ma
from sql.models import Medication, User

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    fields = ("id", "name")

class MedicationSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Medication
    load_instance = True
    
  patient = ma.Nested(UserSchema)
  prescriber = ma.Nested(UserSchema)
  deactivation_reason = ma.String(required=False, allow_none=True)
  
  @validates_schema
  def validate_deactivation_reason(self, data, **kwargs):
    if data.get("active") is False and not data.get("deactivation_reason"):
      raise ValidationError(
        {"deactivation_reason": "Deactivation reason is required when medication is inactive"}
      )

medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)