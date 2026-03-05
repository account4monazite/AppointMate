from enum import Enum
from datetime import datetime
from typing import Optional,List
from pydantic import EmailStr, BaseModel
class UserRole(str, Enum):
    doctor = "doctor"
    patient = "patient"
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    phone: str

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
#enum('Scheduled','Completed','Cancelled','No_Show')
class AppointmentStatus(str,Enum):
    Scheduled="Scheduled"
    Cancelled="Cancelled"
    Completed="Completed"
    No_Show="No_Show"
class AppointmentCreate(BaseModel):
    doc_id: int
    date_time: datetime
    
class AppointmentResponse(BaseModel):
    appt_id: int
    patient_id: int
    doc_id: int
    date_time: datetime
    status: AppointmentStatus
    notes: Optional[str]
    created_at: datetime
    updated_at:datetime

    class Config:
        from_attributes = True
class AppointmentUpdate(BaseModel):
    status: AppointmentStatus

class Tests(str,Enum):
    CT='CT'
    MRI='MRI'
    XRAY='XRAY'
    none='none'
    
class AppointmentResponse(BaseModel):
    appt_id:int
    date_time:datetime
    doc_name:str
    test_type:Tests
    class Config:
        from_attributes=True

class PrescriptionItemResponse(BaseModel):
    medication: str
    dose: str

class PrescriptionResponse(BaseModel):
    appt_id: int
    items: List[PrescriptionItemResponse]

class DashboardResponse(BaseModel):
    current_appointments:List[AppointmentResponse]
    number_current_appts:int
   # total_appointments:List[AppointmentResponse]
    current_tests:List[AppointmentResponse]
    number_current_tests:int
   # total_tests:List[AppointmentResponse]
    prescription: List[PrescriptionResponse] |None
    
    