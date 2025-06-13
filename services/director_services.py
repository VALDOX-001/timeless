from sqlalchemy.orm import Session
from models import Director
import schemas

def create_director(db: Session, director_data: schemas.DirectorCreate):
    directors = Director(
        name=director_data.name,
        date_of_birth=director_data.date_of_birth,
        citizenship=director_data.citizenship
    )
    db.add(directors)
    db.commit()
    db.refresh(directors)
    return directors

def get_directors(skip: int, limit: int, db: Session):
    return db.query(Director).offset(skip).limit(limit).all()

def get_director_by_id(db: Session, director_id: int):
    return db.query(Director).filter(Director.id == director_id).first()

def update_director(db: Session, director_id: int, director_data: schemas.DirectorUpdate):
    director = get_director_by_id(db, director_id)
    if not director:
        return None
    for key, value in director_data.model_dump():
        setattr(director, key, value)
    db.commit()
    db.refresh(director)
    return director

def delete_director(db: Session, director_id: int):
    director = get_director_by_id(db, director_id)
    if not director:
        return {"detail": "Director not found"}
    db.delete(director)
    db.commit()
    return {"detail": "Director deleted successfully"}