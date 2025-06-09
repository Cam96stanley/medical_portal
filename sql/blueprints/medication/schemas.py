from sql.extensions import ma
from sql.models import Medication

class MedicationSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Medication
    load_instance = True

medication_schema = MedicationSchema()
medications_schema = MedicationSchema(many=True)