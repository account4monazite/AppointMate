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
