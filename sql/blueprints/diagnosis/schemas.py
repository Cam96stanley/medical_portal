from marshmallow_sqlalchemy import auto_field
from sql.extensions import ma
from sql.models import Diagnosis
from sql.blueprints.user.schemas import UserSchema

class DiagnosisSchema(ma.SQLAlchemyAutoSchema):
  patient = ma.Nested(UserSchema)
  
  created_at = auto_field(dump_only=True)
  class Meta:
    model = Diagnosis
    load_instance = True
    include_fk = True

diagnosis_schema = DiagnosisSchema()
diagnoses_schema = DiagnosisSchema(many=True)