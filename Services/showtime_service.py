from sqlalchemy.orm import Session
from models import ShowTime
import traceback
import schemas

def create_showtime(db: Session, showtime_data: schemas.ShowTimeCreate):
    showtime = ShowTime(**showtime_data.model_dump())
    db.add(showtime)
    db.commit()
    db.refresh(showtime)
    return showtime

def get_showtime(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ShowTime).offset(skip).limit(limit).all()

def get_showtime_by_id(db: Session, showtime_id: int):
    return db.query(ShowTime).filter(ShowTime.id == showtime_id).first()

def update_showtime(db: Session, showtime_id: int, showtime_data: schemas.ShowTimeUpdate):
    try:
        showtime = get_showtime_by_id(db, showtime_id)
        if not showtime:
            return None
        for key, value in showtime_data.model_dump(exclude_unset=True).items():
            setattr(showtime, key, value)
            db.commit()
            db.refresh(showtime)
        return showtime
    except Exception:
        traceback.print_exc()
        db.rollback()
        return None

def delete_showtime(db: Session, showtime_id: int):
    showtime = get_showtime_by_id(db, showtime_id)
    if not showtime:
        return {"detail": "Showtime not found"}
    db.delete(showtime)
    db.commit()
    return {"detail": "Showtime deleted successfully"}