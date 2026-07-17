from enum import Enum
from datetime import datetime
from typing import Optional
from models import GenderEnum
from pydantic import EmailStr, BaseModel
class UserRole(str, Enum):
    doctor = "doctor"
    patient = "patient"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.patient
    
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True  
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[UserRole] = None

class PatientCreate(BaseModel):
    pat_name: str
    dob: datetime
    gender: GenderEnum
    contact: str
    allergies: Optional[str] = None

class PatientResponse(BaseModel):
    patient_id: int
    pat_name: str
    dob: datetime
    gender: GenderEnum
    contact: str
    allergies: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True

class DoctorCreate(BaseModel):
    email: EmailStr
    password: str
    doc_name: str
    specialization: str
    contact: str

class DoctorResponse(BaseModel):
    doc_id: int
    doc_name: str
    specialization: str
    contact: str
    email: Optional[str] = None

    class Config:
        from_attributes = True
