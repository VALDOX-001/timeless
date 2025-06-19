from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_directors
from Services import director_services

director_router = APIRouter(prefix="/directors", tags=["Directors"])

@director_router.post("/", response_model=schemas.Director)
def create_director(director: schemas.DirectorCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return director_services.create_director(db, director)

@director_router.get("/", response_model=list[schemas.Director])
def list_directors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return director_services.get_directors(db, skip, limit)

@director_router.get("/search", response_model=list[schemas.Director])
def search_directors_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_directors(db=db, keyword=keyword, skip=skip, limit=limit)

@director_router.get("/{director_id}", response_model=schemas.DirectorWithPlays)
def get_director(director_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    director = director_services.get_director_by_id(db, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@director_router.put("/{director_id}", response_model=schemas.Director)
def update_director(director_id: int, director_data: schemas.DirectorUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = director_services.update_director(db, director_id, director_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Director not found")
    return updated

@director_router.delete("/{director_id}")
def delete_director(director_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return director_services.delete_director(db, director_id)
