from sqlalchemy.orm import Session
from models import ShowTime
import schemas


def create_showtime(db: Session, showtime_data: schemas.ShowTimeCreate):
    showtime = ShowTime(
        date_time=showtime_data.date_time,
        play_id=showtime_data.play_id
    )
    db.add(showtime)
    db.commit()
    db.refresh(showtime)
    return showtime


def get_all_showtimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ShowTime).offset(skip).limit(limit).all()


def get_showtime_by_id(db: Session, showtime_id: int):
    return db.query(ShowTime).filter(ShowTime.id == showtime_id).first()


def update_showtime(db: Session, showtime_id: int, showtime_data: schemas.ShowTimeUpdate):
    showtime = get_showtime_by_id(db, showtime_id)
    if not showtime:
        return None
    for key, value in showtime_data.dict(exclude_unset=True).items():
        setattr(showtime, key, value)
    db.commit()
    db.refresh(showtime)
    return showtime


def delete_showtime(db: Session, showtime_id: int):
    showtime = get_showtime_by_id(db, showtime_id)
    if not showtime:
        return False
    db.delete(showtime)
    db.commit()
    return True