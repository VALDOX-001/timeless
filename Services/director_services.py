from sqlalchemy.orm import Session
from models import Director
import traceback
import schemas

def create_director(db: Session, director_data: schemas.DirectorCreate):
    director = Director(**director_data.model_dump())
    db.add(director)
    db.commit()
    db.refresh(director)
    return director

def get_directors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Director).offset(skip).limit(limit).all()

def get_director_by_id(db: Session, director_id: int):
    return db.query(Director).filter(Director.id == director_id).first()

def update_director(db: Session, director_id: int, director_data: schemas.DirectorUpdate):
    try:
        director = get_director_by_id(db, director_id)
        if not director:
            return None
        for key, value in director_data.model_dump(exclude_unset=True).items():
            setattr(director, key, value)
            db.commit()
            db.refresh(director)
            return director

    except Exception:
        traceback.print_exc()
        db.rollback()
        return None
<<<<<<< HEAD:Services/director_services.py


=======
    for key, value in director_data.model_dump().items():
        setattr(director, key, value)
    db.commit()
    db.refresh(director)
    return director
>>>>>>> e038b47b3e33613ad5f25374d83882acc461646c:services/director_services.py

def delete_director(db: Session, director_id: int):
    director = get_director_by_id(db, director_id)
    if not director:
        return {"detail": "Director not found"}
    db.delete(director)
    db.commit()
    return {"detail": "Director deleted successfully"}
