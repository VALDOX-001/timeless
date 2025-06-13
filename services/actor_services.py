from sqlalchemy.orm import Session
from models import Actor
import schemas




def create_actor(db: Session, actor_data: schemas.ActorCreate):
    actors = Actor(
    name= actor_data.name,
    gender=actor_data.gender,
    date_of_birth=actor_data.date_of_birth
    )
    db.add(actors)
    db.commit()
    db.refresh(actors)
    return actors

def get_actors(skip: int, limit: int, db: Session):
    return db.query(Actor).offset(skip).limit(limit).all()


def get_actor_by_id(db: Session, actor_id: int):
    return db.query(Actor).filter(Actor.id == actor_id).first()


def update_actor(db:Session, actor_id: int, actor_data: schemas.ActorUpdate):
    actor = get_actor_by_id(db, actor_id)
    if not actor:
        return None
    for key, value in actor_data.model_dump():
        setattr(actor, key, value)
    db.commit()
    db.refresh(actor)
    return actor

def delete_actor(db: Session, actor_id: int):
    actor = get_actor_by_id(db, actor_id)
    if not actor:
        return {"detail": "Actor not found"}
    db.delete(actor)
    db.commit()
    return {"detail": "Actor deleted successfully"}




