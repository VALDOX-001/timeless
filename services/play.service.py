from sqlalchemy.orm import Session
from models import Play
import schemas


def create_play(db: Session, play_data: schemas.PlayCreate):
    play = Play(
        title=play_data.title,
        duration=play_data.duration,
        genre=play_data.genre,
        synopsis=play_data.synopsis,
        actor_id=play_data.actor_id,
        director_id=play_data.director_id
    )
    db.add(play)
    db.commit()
    db.refresh(play)
    return play


def get_all_plays(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Play).offset(skip).limit(limit).all()


def get_play_by_id(db: Session, play_id: int):
    return db.query(Play).filter(Play.id == play_id).first()


def update_play(db: Session, play_id: int, play_data: schemas.PlayUpdate):
    play = get_play_by_id(db, play_id)
    if not play:
        return None
    for key, value in play_data.dict(exclude_unset=True).items():
        setattr(play, key, value)
    db.commit()
    db.refresh(play)
    return play


def delete_play(db: Session, play_id: int):
    play = get_play_by_id(db, play_id)
    if not play:
        return False
    db.delete(play)
    db.commit()
    return True