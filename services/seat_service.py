from sqlalchemy.orm import Session
from models import Seat
import schema

def create_seat(db: Session, seat_data: schema.SeatCreate):
    seat = Seat(row_number=seat_data.RowNo, seat_number=seat_data.SeatNo)
    db.add(seat)
    db.commit()
    db.refresh(seat)
    return seat

def get_all_seats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Seat).offset(skip).limit(limit).all()

def get_seat_by_id(db: Session, seat_id: int):
    return db.query(Seat).filter(Seat.id == seat_id).first()

def update_seat(db: Session, seat_id: int, seat_data: schema.SeatUpdate):
    seat = get_seat_by_id(db, seat_id)
    if not seat:
        return None
    if seat_data.RowNo is not None:
        seat.row_number = seat_data.RowNo
    if seat_data.SeatNo is not None:
        seat.seat_number = seat_data.SeatNo
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
