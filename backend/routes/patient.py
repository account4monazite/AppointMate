from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.user_schemas import PatientCreate, PatientResponse
from auth.jwt_auth import get_current_user

router = APIRouter()

@router.post("/patient/profile")
async def create_patient_profile(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    existing = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    if current_user.role not in (models.UserRole.patient, "patient"):
        raise HTTPException(status_code=403, detail=f"Not authorized. Your role: {current_user.role}")

    patient = models.Patient(
        pat_name=data.pat_name,
        dob=data.dob,
        gender=data.gender,
        contact=data.contact,
        user_id=current_user.user_id
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {"message": "Profile created successfully"}

@router.get("/patient/profile", response_model=PatientResponse)
async def get_patient_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Profile not found")

    return patient

@router.put("/patient/profile")
async def update_patient_profile(
    data: PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Profile not found")

    patient.pat_name = data.pat_name
    patient.dob = data.dob
    patient.gender = data.gender
    patient.contact = data.contact

    db.commit()
    db.refresh(patient)

    return {"message": "Profile updated successfully"}