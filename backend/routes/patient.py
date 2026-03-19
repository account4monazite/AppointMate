from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.user_schemas import PatientCreate
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

    if current_user.role != models.UserRole.patient:
        raise HTTPException(status_code=403, detail="Not authorized")

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