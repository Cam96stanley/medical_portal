from marshmallow import EXCLUDE
from sql.extensions import ma
from sql.models import BloodPressure, HeartRate, Weight, Glucose, Temperature

class BloodPressureSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = BloodPressure
    load_instance = True
    unknown = EXCLUDE
    
  recorded_at = ma.auto_field(dump_only=True)


class HeartRateSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = HeartRate
    load_instance = True
    unknown = EXCLUDE
    
  recorded_at = ma.auto_field(dump_only=True)


class WeightSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Weight
    load_instance = True
    unknown = EXCLUDE
    
  recorded_at = ma.auto_field(dump_only=True)


class GlucoseSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Glucose
    load_instance = True
    unknown = EXCLUDE
    
  recorded_at = ma.auto_field(dump_only=True)


class TemperatureSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Temperature
    load_instance = True
    unknown = EXCLUDE
    
  recorded_at = ma.auto_field(dump_only=True)


bloodpressure_schema = BloodPressureSchema()
heartrate_schema = HeartRateSchema()
weight_schema = WeightSchema()
glucose_schema = GlucoseSchema()
temperature_schema = TemperatureSchema()