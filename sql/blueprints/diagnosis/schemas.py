from sql.extensions import ma
from sql.models import Diagnosis
from sql.blueprints.user.schemas import UserSchema

class DiagnosisSchema(ma.SQLAlchemyAutoSchema):
  patient = ma.Nested(UserSchema)
  class Meta:
    model = Diagnosis
    load_instance = True
    include_fk = True

diagnosis_schema = DiagnosisSchema()
diagnoses_schema = DiagnosisSchema(many=True)