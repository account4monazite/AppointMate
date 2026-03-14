from datetime import datetime, time, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
from database import get_db

router = APIRouter()


def calculate_available_slots(doc_id: int, selected_date: datetime.date, db: Session):
    start_time = datetime.combine(selected_date, time(9, 0))
    end_time = datetime.combine(selected_date, time(19, 0))
    slot_duration = timedelta(minutes=30)

    all_slots = []
    current = start_time
    while current < end_time:
        all_slots.append(current)
        current += slot_duration

    booked = db.query(models.AppointmentTest.date_time).filter(
        models.AppointmentTest.doc_id == doc_id,
        models.AppointmentTest.date_time >= start_time,
        models.AppointmentTest.date_time < end_time,
        models.AppointmentTest.status == "Scheduled"
    ).all()

    booked_slots = {b.date_time for b in booked}
    return [slot for slot in all_slots if slot not in booked_slots]


@router.get("/doctors/{doc_id}/available-slots")
def get_available_slots(doc_id: int, date: str, db: Session = Depends(get_db)):
    selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    available_slots = calculate_available_slots(doc_id, selected_date, db)
    return {
        "doctor_id": doc_id,
        "date": date,
        "available_slots": available_slots
    }