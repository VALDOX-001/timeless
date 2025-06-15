from sqlalchemy.orm import Session
from models import Seat
import traceback
import schemas

def create_seat(db: Session, seat_data: schemas.SeatCreate):
    seat = Seat(**seat_data.model_dump())
    db.add(seat)
    db.commit()
    db.refresh(seat)
    return seat

def get_seats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Seat).offset(skip).limit(limit).all()

def get_seat_by_id(db: Session, seat_id: int):
    return db.query(Seat).filter(Seat.id == seat_id).first()

def update_seat(db: Session, seat_id: int, seat_data: schemas.SeatUpdate):
    try:
        seat = get_seat_by_id(db, seat_id)
        if not seat:
            return None
        for key, value in seat_data.model_dump(exclude_unset=True).items():
            setattr(seat, key, value)
            db.commit()
            db.refresh(seat)
            return seat
    except Exception:
        traceback.print_exc()
        db.rollback()
        return None

def delete_seat(db: Session, seat_id: int):
    seat = get_seat_by_id(db, seat_id)
    if not seat:
        return {"detail": "Seat not found"}
    db.delete(seat)
    db.commit()
    return {"detail": "Seat deleted successfully"}