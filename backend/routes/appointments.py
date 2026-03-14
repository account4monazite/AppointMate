from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter,Depends,HTTPException
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from database import get_db
import models
from schemas.appointment import AppointmentRequest,AppointmentUpdate


@router.post("/bookAppointment/{doc_id}")
async def book_appt(doc_id: int, data:AppointmentRequest,db:Session=Depends(get_db)):
    now=datetime.datetime.now()
    appointment=models.AppointmentTest(**data.model_dump(), test_type='none', created_at=now, updated_at=now)
    db.add(appointment)
    try: db.commit()
    except IntegrityError:
        db.rollback()
        return{"error":"time slot if already booked"}
    return appointment


@router.post("/bookTest/{doc_id}")
async def book_appt(doc_id:int,test_type:str, data:AppointmentRequest,db:Session=Depends(get_db)):
    now=datetime.datetime.now()
    test_type = test_type.strip("'\"")
    appointment=models.AppointmentTest(**data.model_dump(),
       test_type=test_type,
        created_at=now, updated_at=now)
    db.add(appointment)
    try: db.commit()
    except IntegrityError:
        db.rollback()
        return{"error":"time slot if already booked"}
    return appointment

@router.patch("/update_appt/{appt_id}")
async def update_appts(appt_id:int,date_time:datetime,data:AppointmentUpdate,db:Session=Depends(get_db)):
    now=datetime.now()
    appt =db.query(models.AppointmentTest).filter(
    models.AppointmentTest.appt_id==appt_id,
    models.AppointmentTest.test_type=="none").first()
    
    if not appt:
        raise HTTPException(status_code=404,detail="Appointment not found")  
    
    time_diff=appt.date_time-now
    if time_diff<timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot update appoinment within 24 hours"
        )        
        
    appt.date_time=date_time
    db.commit()
    db.refresh(appt)
    
    return {'message':"appointment updated successfully"}                       


@router.patch("/update_test/{appt_id}")
async def update_tests(appt_id:int,date_time:datetime,data:AppointmentUpdate,db:Session=Depends(get_db)):
    now=datetime.now()
    appt =db.query(models.AppointmentTest).filter(
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
        
    appt.date_time=date_time
    db.commit()
    db.refresh(appt)
    
    return {'changed':data}     

@router.delete("/delete_appt/{appt_id}")
async def delete_appts(appt_id:int,db:Session=Depends(get_db)):
    appt =db.query(models.AppointmentTest).filter(
    models.AppointmentTest.appt_id==appt_id,
    models.AppointmentTest.test_type=="none").first()
    
    if not appt:
        raise HTTPException(status_code=404,detail="Appointment not found")  
    
    time_diff=appt.date_time-datetime.now()
    if time_diff<timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel appoinment within 24 hours"
        )        
    db.delete(appt)   
    db.commit()
    
    return{"Message":"Appointment cancelled"}          
                                       

@router.delete("/delete_test/{appt_id}")
async def delete_tests(appt_id:int,db:Session=Depends(get_db)):
    appt =db.query(models.AppointmentTest).filter(
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
    db.delete(appt)   
    db.commit()
    
    return{"Message":"Test cancelled"}                                           