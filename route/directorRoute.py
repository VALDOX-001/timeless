from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
from database import get_db
from Services import director_services

director_router = APIRouter(prefix="/directors", tags=["Directors"])


@director_router.post("/", response_model=schemas.Director)
def create_director(
    director: schemas.DirectorCreate,
    db: Session = Depends(get_db)
):
    return director_services.create_director(db, director)


@director_router.get("/", response_model=List[schemas.Director])
def list_directors(
    skip: int = 0,
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search directors by name"),
    db: Session = Depends(get_db)
):
    return director_services.get_directors(db=db, skip=skip, limit=limit, search=search)


@director_router.get("/{director_id}", response_model=schemas.Director)
def get_director(director_id: int, db: Session = Depends(get_db)):
    director = director_services.get_director_by_id(db, director_id)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director


@director_router.put("/{director_id}", response_model=schemas.Director)
def update_director(
    director_id: int,
    director_data: schemas.DirectorUpdate,
    db: Session = Depends(get_db)
):
    updated_director = director_services.update_director(db, director_id, director_data)
    if not updated_director:
        raise HTTPException(status_code=404, detail="Director not found or update failed")
    return updated_director


@director_router.delete("/{director_id}", response_model=dict)
def delete_director(director_id: int, db: Session = Depends(get_db)):
    success = director_services.delete_director(db, director_id)
    if not success:
        raise HTTPException(status_code=404, detail="Director not found or already deleted")
    return {"detail": "Director deleted successfully"}
