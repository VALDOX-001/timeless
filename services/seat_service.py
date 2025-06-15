from sqlalchemy.orm import Session
from models import Seat
import schemas  # fixed import

def create_seat(db: Session, seat_data: schemas.SeatCreate):
    seat = Seat(row_number=seat_data.row_number, seat_number=seat_data.seat_number)
    db.add(seat)
    db.commit()
    db.refresh(seat)
    return seat

def get_all_seats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Seat).offset(skip).limit(limit).all()

def get_seat_by_id(db: Session, seat_id: int):
    return db.query(Seat).filter(Seat.id == seat_id).first()

def update_seat(db: Session, seat_id: int, seat_data: schemas.SeatUpdate):
    seat = get_seat_by_id(db, seat_id)
    if not seat:
        return None
    for key, value in seat_data.model_dump(exclude_unset=True).items():
        if key == "row_number":
            seat.row_number = value
        elif key == "seat_number":
            seat.seat_number = value
    db.commit()
    db.refresh(seat)
    return seat

def delete_seat(db: Session, seat_id: int):
    seat = get_seat_by_id(db, seat_id)
    if not seat:
        return False
    db.delete(seat)
    db.commit()
    return True
