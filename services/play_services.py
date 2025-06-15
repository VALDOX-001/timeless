from sqlalchemy.orm import Session
from models import Play
import traceback
import schemas

def create_play(db: Session, play_data: schemas.PlayCreate):
    play = Play(**play_data.model_dump())
    db.add(play)
    db.commit()
    db.refresh(play)
    return play


def get_plays(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Play).offset(skip).limit(limit).all()

def get_play_by_id(db: Session, play_id: int):
    return db.query(Play).filter(Play.id == play_id).first()

def update_play(db: Session, play_id: int, play_data: schemas.PlayUpdate):
    try:
        play = get_play_by_id(db, play_id)
        if not play:
            return None
        for key, value in play_data.model_dump(exclude_unset=True).items():
            setattr(play, key, value)
            db.commit()
            db.refresh(play)
            return play

    except Exception:
        traceback.print_exc()
        db.rollback()
        return None

def delete_play(db: Session, play_id: int):
    play = get_play_by_id(db, play_id)
    if not play:
        return {"detail": "Play not found"}
    db.delete(play)
    db.commit()
    return {"detail": "Play deleted successfully"}