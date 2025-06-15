from sqlalchemy.orm import Session
from models import Actor
import traceback
import schemas

def create_actor(db: Session, actor_data: schemas.ActorCreate):
    actor = Actor(**actor_data.model_dump())
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor

def get_actors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Actor).offset(skip).limit(limit).all()

def get_actor_by_id(db: Session, actor_id: int):
    return db.query(Actor).filter(Actor.id == actor_id).first()


def update_actor(db: Session, actor_id: int, actor_data: schemas.ActorUpdate):
    try:
        actor = get_actor_by_id(db, actor_id)
        if not actor:
            return None
        for key, value in actor_data.model_dump(exclude_unset=True).items():
            setattr(actor, key, value)
            db.commit()
            db.refresh(actor)
            return actor
    except Exception:
        traceback.print_exc()
        db.rollback()
        return None


def delete_actor(db: Session, actor_id: int):
    actor = get_actor_by_id(db, actor_id)
    if not actor:
        return {"detail": "Actor not found"}
    db.delete(actor)
    db.commit()
    return {"detail": "Actor deleted successfully"}