from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.appointment import AppointmentRequest, AppointmentUpdate
from auth.jwt_auth import get_current_user
from .doctors import calculate_available_slots

router = APIRouter()

@router.post("/bookAppointment/{doc_id}")
async def book_appt(
    doc_id: int,
    data: AppointmentRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # get slots for selected date
    date = data.date_time.date()

    available_slots = calculate_available_slots(doc_id, date, db)

    if data.date_time not in available_slots:
        raise HTTPException(status_code=400, detail="Slot not available")

    now = datetime.now()

    appointment = models.AppointmentTest(
        **data.model_dump(),
        doc_id=doc_id,
        patient_id=patient.patient_id,
        test_type="none",
        created_at=now,
        updated_at=now
    )

    db.add(appointment)

    try:
        db.commit()
        db.refresh(appointment)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Time slot already booked"
        )

    return appointment

@router.post("/bookTest/{doc_id}")
async def book_appt(doc_id:int,
        test_type:str, 
        data:AppointmentRequest,
        db:Session=Depends(get_db),
        current_user=Depends(get_current_user)):
    
    patient=db.query(models.Patient).filter(
        models.Patient.user_id==current_user.user_id
        ).first()
    
    if not patient:
        raise HTTPException(status_code=404,detail="patient not found")
    
    date = data.date_time.date()

    available_slots = calculate_available_slots(doc_id, date, db)

    if data.date_time not in available_slots:
        raise HTTPException(status_code=400, detail="Slot not available")

    now = datetime.now()
    test_type = test_type.strip("'\"")
    appointment=models.AppointmentTest(**data.model_dump(),
       doc_id=doc_id,
       patient_id=patient.patient_id,                               
       test_type=test_type,
        created_at=now, updated_at=now)
    db.add(appointment)
    try: db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Time slot already booked"
        )       
    return appointment

@router.patch("/appointment/{appt_id}")
async def update_appts(
    appt_id: int,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    now = datetime.now()

    appt = db.query(models.AppointmentTest).filter(
        models.AppointmentTest.patient_id == patient.patient_id,
        models.AppointmentTest.appt_id == appt_id,
        models.AppointmentTest.test_type == "none"
    ).first()

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # prevent update within 24 hours
    if appt.date_time - now < timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot update appointment within 24 hours"
        )

    # check new slot availability
    date = data.date_time.date()
    available_slots = calculate_available_slots(data.doc_id, date, db)

    if data.date_time not in available_slots:
        raise HTTPException(status_code=400, detail="Slot not available")

    # update appointment
    appt.doc_id = data.doc_id
    appt.date_time = data.date_time
    appt.updated_at = now

    try:
        db.commit()
        db.refresh(appt)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Time slot already booked"
        )

    return {"message": "Appointment updated successfully"}

@router.patch("/update_test/{appt_id}")
async def update_tests(appt_id:int,date_time:datetime,data:AppointmentUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    now=datetime.now()
    appt =db.query(models.AppointmentTest).filter(
    models.AppointmentTest.patient_id == patient.patient_id,
    models.AppointmentTest.appt_id==appt_id,
    models.AppointmentTest.test_type!="none").first()
    
    if not appt:
        raise HTTPException(status_code=404,detail="Test not found")  
    
    time_diff=appt.date_time-now
    if time_diff<timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot update Test timings within 24 hours"
        )        
    date = data.date_time.date()
    available_slots = calculate_available_slots(data.doc_id, date, db)

    if data.date_time not in available_slots:
        raise HTTPException(status_code=400, detail="Slot not available")

    appt.doc_id = data.doc_id
    appt.date_time = data.date_time
    appt.updated_at = now
    try:
            db.commit()
            db.refresh(appt)

    except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Time slot already booked"
            )

    return {"message": "TEST updated successfully"}   

@router.delete("/delete_appt/{appt_id}")
async def delete_appts(appt_id:int,
        db:Session=Depends(get_db),
        current_user=Depends(get_current_user)
        ):
    
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    now = datetime.now()
    
    appt =db.query(models.AppointmentTest).filter(
    models.AppointmentTest.patient_id == patient.patient_id,
    models.AppointmentTest.appt_id==appt_id,
    models.AppointmentTest.test_type=="none").first()
    
    if not appt:
        raise HTTPException(status_code=404,detail="Appointment not found")  
    
    time_diff=appt.date_time-now
    if time_diff<timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel appointment within 24 hours"
        ) 
    appt.status=models.AppointmentStatus.Cancelled
    appt.updated_at=now     
    db.commit()
    db.refresh(appt)
    
    return{"Message":"Appointment cancelled"}          
                                       

@router.delete("/delete_test/{appt_id}")
async def delete_tests(appt_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    now=datetime.now()
    appt =db.query(models.AppointmentTest).filter(
    models.AppointmentTest.patient_id == patient.patient_id,    
    models.AppointmentTest.appt_id==appt_id,
    models.AppointmentTest.test_type!="none").first()
    
    if not appt:
        raise HTTPException(status_code=404,detail="Test not found")  
    
    time_diff=appt.date_time-datetime.now()
    if time_diff<timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel Test within 24 hours"
        )        
    appt.status=models.AppointmentStatus.Cancelled
    appt.updated_at=now     
    db.commit()
    db.refresh(appt)
    return{"Message":"Test cancelled"}         

@router.get("/history")
async def get_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(
        models.Patient.user_id == current_user.user_id
    ).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    now = datetime.now()

    past_appts = db.query(models.AppointmentTest).filter(
        models.AppointmentTest.patient_id == patient.patient_id,
        models.AppointmentTest.date_time < now
    ).order_by(models.AppointmentTest.date_time.desc()).all()

    return past_appts                                  