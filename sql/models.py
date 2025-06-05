from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum, Date, DateTime
from datetime import date, datetime, timezone
import enum

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class UserRole(enum.Enum):
  PATIENT = "patient"
  DOCTOR = "doctor"
  
class AppointmentStatus(enum.Enum):
  SCHEDULED = "scheduled"
  COMPLETED = "completed"
  CANCELLED = "cancelled"
  NO_SHOW = "no_show"

class User(db.Model):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(db.String(100), nullable=False)
  email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(db.String(150), nullable=False)
  
  role: Mapped[UserRole] = mapped_column(Enum(UserRole), default="patient", nullable=False)


class Diagnosis(db.Model):
  __tablename__ = "diagnosis"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  diagnosis_name: Mapped[str] = mapped_column(db.String(150), nullable=False)
  diagnosis_code: Mapped[str] = mapped_column(db.String(50))
  
  diagnosis_date: Mapped[date] = mapped_column(Date, nullable=False)
  notes: Mapped[str] = mapped_column(db.String(5000), nullable=False)
  
  patient = db.relationship("User", backref="diagnoses", foreign_keys=[patient_id])


class Medication(db.Model):
  __tablename__ = "medications"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  name: Mapped[str] = mapped_column(db.String(150), nullable=False)
  dosage: Mapped[str] = mapped_column(db.String(100))
  frequency: Mapped[str] = mapped_column(db.String(100))
  
  prescribed_by_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=True)
  prescribed_by_name: Mapped[str] = mapped_column(db.String(150), nullable=True)
  
  patient = db.relationship("User", foreign_keys=[patient_id], backref="medications")
  prescriber = db.relationship("User", foreign_keys=[prescribed_by_id])


class Notifications(db.Model):
  __tablename__ = "notifications"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  message: Mapped[str] = mapped_column(db.String(1000), nullable=False)
  is_read: Mapped[bool] = mapped_column(db.Boolean(), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                              nullable=False,
                                              default=lambda: datetime.now(timezone.utc)
                                              )
  
  user = db.relationship("User", backref="notifications")


class Appointment(db.Model):
  __tablename__ = "appointments"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  doctor_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  appointment_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
  notes: Mapped[str] = mapped_column(db.String(1000), nullable=False)
  status: Mapped[AppointmentStatus] = mapped_column(
                                              Enum(AppointmentStatus),
                                              nullable=False,
                                              default=AppointmentStatus.SCHEDULED
                                              )
  reason: Mapped[str] = mapped_column(db.String(250))
  
  patient = db.relationship("User", foreign_keys=[patient_id], backref="patient_appointments")
  doctor = db.relationship("User", foreign_keys=[doctor_id], backref="doctor_appointments")


class Goal(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  created_by: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  title: Mapped[str] = mapped_column(db.String(100), nullable=False)
  description: Mapped[str] = mapped_column(db.String(250), nullable=False)
  
  target_date: Mapped[date] = mapped_column(Date, nullable=False)
  is_complete: Mapped[bool] = mapped_column(db.Boolean(), default=False)
  
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                              nullable=False,
                                              default=lambda: datetime.now(timezone.utc)
                                              )
  
  patient = db.relationship("User", foreign_keys=[patient_id], backref="goals")
  creator = db.relationship("User", foreign_keys=[created_by], backref="created_goals")


class BloodPressure(db.Model):
  __tablename__ = "blood_pressures"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  systolic: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  diastolic: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  
  recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                              nullable=False,
                                              default=lambda: datetime.now(timezone.utc)
                                              )
  
  patient = db.relationship("User", backref="blood_pressures", foreign_keys=[patient_id])


class HeartRate(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  value: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  
  recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                            nullable=False,
                                            default=lambda: datetime.now(timezone.utc)
                                            )
  
  patient = db.relationship("User", backref="heart_rates", foreign_keys=[patient_id])


class Weight(db.Model):
  __tablename__ = "weights"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  value: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  
  recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                            nullable=False,
                                            default=lambda: datetime.now(timezone.utc)
                                            )
  
  patient = db.relationship("User", backref="weights", foreign_keys=[patient_id])


class Glucose(db.Model):
  __tablename__ = "glucose"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  value: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  
  recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                            nullable=False,
                                            default=lambda: datetime.now(timezone.utc)
                                            )
  
  patient = db.relationship("User", backref="glucose_readings", foreign_keys=[patient_id])


class Temperature(db.Model):
  __tablename__ = "temperatures"
  
  id: Mapped[int] = mapped_column(primary_key=True)
  patient_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False)
  
  value: Mapped[float] = mapped_column(db.Float(), nullable=False)
  
  recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                            nullable=False,
                                            default=lambda: datetime.now(timezone.utc)
                                            )
  
  patient = db.relationship("User", backref="temperature_readings", foreign_keys=[patient_id])