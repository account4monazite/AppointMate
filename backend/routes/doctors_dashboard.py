from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Doctor, AppointmentTest, Patient, UserRole, AppointmentStatus
from auth.jwt_auth import get_current_user
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/doctor", tags=["Doctor Portal"])

class PatientDetails(BaseModel):
    patient_id: int
    pat_name: str
    dob: datetime
    gender: str
    contact: str
    allergies: str | None = None

class DoctorAppointmentResponse(BaseModel):
    appt_id: int
    date_time: datetime
    test_type: str
    status: str
    reason: str | None = None
    patient: PatientDetails

def verify_doctor(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.doctor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Doctor role required."
        )
    doctor = db.query(Doctor).filter(Doctor.user_id == current_user.user_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor profile not found."
        )
    return doctor

@router.get("/appointments", response_model=List[DoctorAppointmentResponse])
def get_doctor_appointments(doctor: Doctor = Depends(verify_doctor), db: Session = Depends(get_db)):
    appointments = db.query(AppointmentTest).filter(
        AppointmentTest.doc_id == doctor.doc_id
    ).order_by(AppointmentTest.date_time.asc()).all()

    result = []
    for appt in appointments:
        pat = db.query(Patient).filter(Patient.patient_id == appt.patient_id).first()
        if not pat:
            continue
        
        pat_details = PatientDetails(
            patient_id=pat.patient_id,
            pat_name=pat.pat_name,
            dob=pat.dob,
            gender=pat.gender,
            contact=pat.contact,
            allergies=pat.allergies
        )

        result.append(
            DoctorAppointmentResponse(
                appt_id=appt.appt_id,
                date_time=appt.date_time,
                test_type=appt.test_type.value if hasattr(appt.test_type, "value") else str(appt.test_type),
                status=appt.status.value if hasattr(appt.status, "value") else str(appt.status),
                reason=appt.reason,
                patient=pat_details
            )
        )
    return result

@router.post("/appointments/{appt_id}/complete")
def complete_appointment(appt_id: int, doctor: Doctor = Depends(verify_doctor), db: Session = Depends(get_db)):
    appt = db.query(AppointmentTest).filter(
        AppointmentTest.appt_id == appt_id,
        AppointmentTest.doc_id == doctor.doc_id
    ).first()

    if not appt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found or not assigned to this doctor."
        )

    appt.status = AppointmentStatus.Completed
    appt.updated_at = datetime.now()
    db.commit()
    db.refresh(appt)

    return {"message": "Appointment marked as completed successfully."}
