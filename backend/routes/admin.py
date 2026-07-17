from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Doctor, UserRole
from schemas.user_schemas import DoctorCreate, DoctorResponse
from auth.jwt_auth import get_current_user, hash_password
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

def verify_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden. Admin role required."
        )
    return current_user

@router.get("/doctors", response_model=List[DoctorResponse], dependencies=[Depends(verify_admin)])
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).all()
    # Populate email from User table for response
    result = []
    for d in doctors:
        email = None
        if d.user:
            email = d.user.email
        result.append(
            DoctorResponse(
                doc_id=d.doc_id,
                doc_name=d.doc_name,
                specialization=d.specialization,
                contact=d.contact,
                email=email
            )
        )
    return result

@router.post("/doctors", response_model=DoctorResponse, dependencies=[Depends(verify_admin)])
def add_doctor(data: DoctorCreate, db: Session = Depends(get_db)):
    # Check if user already exists with this email
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # 1. Create User
    hashed_pw = hash_password(data.password)
    user = User(
        email=data.email,
        hashed_password=hashed_pw,
        role=UserRole.doctor,
        is_active=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2. Create Doctor Profile
    doctor = Doctor(
        doc_name=data.doc_name,
        specialization=data.specialization,
        contact=data.contact,
        user_id=user.user_id
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return DoctorResponse(
        doc_id=doctor.doc_id,
        doc_name=doctor.doc_name,
        specialization=doctor.specialization,
        contact=doctor.contact,
        email=user.email
    )

@router.delete("/doctors/{doc_id}", dependencies=[Depends(verify_admin)])
def remove_doctor(doc_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.doc_id == doc_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found."
        )

    user = doctor.user

    # Delete doctor profile
    db.delete(doctor)
    
    # Delete doctor user account if exists
    if user:
        db.delete(user)
        
    db.commit()
    return {"message": "Doctor and associated user account removed successfully."}
