from schemas.appointment import DashboardResponse
from fastapi import APIRouter,Depends,HTTPException
from models import AppointmentTest,Doctor,Prescription,Patient
import datetime
from sqlalchemy.orm import Session
from database import get_db
from auth.jwt_auth import get_current_user

router=APIRouter()

@router.get("/dashboard",response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    now = datetime.datetime.now()
    patient=db.query(Patient).filter(
        Patient.user_id==current_user.user_id
        ).first()
    
    if not patient:
        raise HTTPException(status_code=404,detail="patient not found")
    
    appt_query = (
        db.query(AppointmentTest, Doctor.doc_name)
        .join(Doctor, AppointmentTest.doc_id == Doctor.doc_id)
        .filter(
            AppointmentTest.patient_id == patient.patient_id,
            AppointmentTest.date_time >= now,
            AppointmentTest.test_type == "none",
            AppointmentTest.status == "Scheduled",
        )
    )
    num_appts = appt_query.count()
    appts = appt_query.all()  
    test_query = (
        db.query(AppointmentTest, Doctor.doc_name)
        .join(Doctor, AppointmentTest.doc_id == Doctor.doc_id)
        .filter(
            AppointmentTest.patient_id == patient.patient_id,
            AppointmentTest.date_time >= now,
            AppointmentTest.test_type != "none",
            AppointmentTest.status == "Scheduled",
        )
    )
    num_tests = test_query.count()
    tests = test_query.all()
    prescription_objs = db.query(Prescription).join(AppointmentTest, Prescription.appt_id == AppointmentTest.appt_id).filter(AppointmentTest.patient_id == patient.patient_id).all()
    prescription_list = []
    for p in prescription_objs:
        items = []
        for m, d in zip(p.medications, p.dosages):
            items.append({"medication": m.medication, "dose": d.dosage})
        prescription_list.append({"appt_id": p.appt_id, "items": items})

    def _appt_to_dict(a_tuple):
        if isinstance(a_tuple, tuple):
            appt, doc_name = a_tuple
        else:
            appt, doc_name = a_tuple, None
        return {
            "appt_id": appt.appt_id,
            "date_time": appt.date_time,
            "doc_name": doc_name,
            "test_type": appt.test_type,
        }

    return {
        "current_appointments": [_appt_to_dict(a) for a in appts],
        "number_current_appts": num_appts,
        "current_tests": [_appt_to_dict(t) for t in tests],
        "number_current_tests": num_tests,
        "prescription": prescription_list or None,
    }
