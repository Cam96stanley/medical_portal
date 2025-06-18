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

medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)