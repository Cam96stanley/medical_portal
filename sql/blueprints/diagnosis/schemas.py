from marshmallow_sqlalchemy import auto_field
from marshmallow import fields
from sql.extensions import ma
from sql.models import Diagnosis
from sql.blueprints.user.schemas import UserSchema

class DiagnosisSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Diagnosis
    load_instance = True
    include_fk = True
    
  patient = fields.Nested(UserSchema(only=("id", "name")))
  doctor = fields.Nested(UserSchema(only=("id", "name")))
  
  created_at = auto_field(dump_only=True)
  diagnosis_name = auto_field()
  diagnosis_code = auto_field()
  diagnosis_date = auto_field()
  notes = auto_field()
  id = auto_field()

diagnosis_schema = DiagnosisSchema()
diagnoses_schema = DiagnosisSchema(many=True)