from database import engine
from user_schemas import DashboardResponse
from models import AppointmentTest,PrescriptionDosage,PrescriptionMedication,Doctor,Prescription
from sqlalchemy.orm import Session
from database import SessionLocal
import datetime
from fastapi import FastAPI,HTTPException,Depends

#Base.metadata.create_all(bind=engine)
app=FastAPI()

current_date=datetime.datetime.now()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/P_dashboard",response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    now = datetime.datetime.now()

    appt_query = (
        db.query(AppointmentTest, Doctor.doc_name)
        .join(Doctor, AppointmentTest.doc_id == Doctor.doc_id)
        .filter(
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
            AppointmentTest.date_time >= now,
            AppointmentTest.test_type != "none",
            AppointmentTest.status == "Scheduled",
        )
    )
    num_tests = test_query.count()
    tests = test_query.all()
    prescription_objs = db.query(Prescription).all()
    prescription_list = []
    for p in prescription_objs:
        items = []
        for m, d in zip(p.medications, p.dosages):
            items.append({"medication": m.medication, "dose": d.dosage})
        prescription_list.append({"appt_id": p.appt_id, "items": items})

    def _appt_to_dict(a_tuple):
        # when joined, the query returns (AppointmentTest, doc_name)
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
    
#so shts getting confusing
#what we're gonna do is make a dashboard response model in schemas
# and then make the query like wise
#cuz im lost here a little
    


