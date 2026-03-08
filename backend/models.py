from sqlalchemy import Column, Integer, String, DateTime, Date, Enum, ForeignKey, TIMESTAMP,UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"
    
class GenderEnum(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    other = "other"

class TestTypeEnum(str, enum.Enum):
    CT = "CT"
    XRAY = "XRAY"
    MRI = "MRI"
    none = "none"

class AppointmentStatus(str, enum.Enum):
    Scheduled = "Scheduled"
    Completed = "Completed"
    Cancelled = "Cancelled"
    No_Show = "No Show"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)
    
class Doctor(Base):
    __tablename__ = "doctor"

    doc_id = Column(Integer, primary_key=True, index=True)
    doc_name = Column(String(100), nullable=False)
    specialization = Column(String(200), nullable=False)
    contact = Column(String(150), nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)

    user = relationship("User", back_populates="doctor")

    contacts = relationship("DoctorContact", back_populates="doctor")
    
class DoctorContact(Base):
    __tablename__ = "doctor_contact"

    contact = Column(String(100), primary_key=True)
    doc_id = Column(Integer, ForeignKey("doctor.doc_id"), primary_key=True)

    doctor = relationship("Doctor", back_populates="contacts")

class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(Integer, primary_key=True, index=True)
    pat_name = Column(String(100), nullable=False)
    dob = Column(DateTime, nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)
    contact = Column(String(150), nullable=False)

    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)

    user = relationship("User", back_populates="patient")

    contacts = relationship("PatientContact", back_populates="patient")

class PatientContact(Base):
    __tablename__ = "patient_contact"

    contact = Column(String(100), primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.patient_id"), primary_key=True)

    patient = relationship("Patient", back_populates="contacts")

class AppointmentTest(Base):
    __tablename__ = "appointment_test"

    appt_id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    test_type = Column(Enum(TestTypeEnum))
    status = Column(Enum(AppointmentStatus),default='Scheduled')

    doc_id = Column(Integer, ForeignKey("doctor.doc_id"))
    patient_id = Column(Integer, ForeignKey("patient.patient_id"))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    prescriptions = relationship("Prescription", back_populates="appointment")
    __table_args__=(UniqueConstraint('date_time','doc_id',name='unique_time_slot'),)

class Prescription(Base):
    __tablename__ = "prescription"

    prescription_id = Column(Integer, primary_key=True, index=True)
    date_issued = Column(Date)

    appt_id = Column(Integer, ForeignKey("appointment_test.appt_id"))

    appointment = relationship("AppointmentTest", back_populates="prescriptions")
    medications = relationship("PrescriptionMedication", back_populates="prescription")
    dosages = relationship("PrescriptionDosage", back_populates="prescription")

class PrescriptionMedication(Base):
    __tablename__ = "prescription_medication"

    medication = Column(String(50), primary_key=True)
    prescription_id = Column(Integer, ForeignKey("prescription.prescription_id"), primary_key=True)

    prescription = relationship("Prescription", back_populates="medications")

class PrescriptionDosage(Base):
    __tablename__ = "prescription_dosage"

    dosage = Column(String(50), primary_key=True)
    prescription_id = Column(Integer, ForeignKey("prescription.prescription_id"), primary_key=True)

    prescription = relationship("Prescription", back_populates="dosages")

