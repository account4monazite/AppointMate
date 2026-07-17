from enum import Enum
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class AppointmentStatus(str,Enum):
    Scheduled="Scheduled"
    Cancelled="Cancelled"
    Completed="Completed"
    No_Show="No_Show"

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
    reason: Optional[str] = None
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
    


class AppointmentRequest(BaseModel):
    doc_id:int
    patient_id:Optional[int] = None
    date_time:datetime
    test_type:Tests
    reason: Optional[str] = None
    

class TestRequest(BaseModel):
    doc_id:int
    patient_id:Optional[int] = None
    date_time:datetime
    test_type:Tests
    reason: Optional[str] = None

class AppointmentUpdate(BaseModel):
    doc_id:int
    date_time:datetime