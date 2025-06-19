from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_showtimes
from Services import showtime_service

showtime_router = APIRouter(prefix="/showtimes", tags=["ShowTimes"])

@showtime_router.post("/", response_model=schemas.ShowTime)
def create_showtime(showtime: schemas.ShowTimeCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return showtime_service.create_showtime(db, showtime)

@showtime_router.get("/", response_model=list[schemas.ShowTime])
def list_showtime(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return showtime_service.get_showtime(db, skip, limit)

@showtime_router.get("/search", response_model=list[schemas.ShowTime])
def search_showtime_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_showtimes(db=db, keyword=keyword, skip=skip, limit=limit)


@showtime_router.get("/{showtime_id}", response_model=schemas.ShowTimeWithPlay)
def get_showtime(showtime_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    showtime = showtime_service.get_showtime_by_id(db, showtime_id)
    if not showtime: raise HTTPException(status_code=404, detail="ShowTime not found")
    return showtime

@showtime_router.put("/{showtime_id}", response_model=schemas.ShowTime)
def update_showtime(showtime_id: int, showtime_data: schemas.ShowTimeUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = showtime_service.update_showtime(db, showtime_id, showtime_data)
    if not updated: raise HTTPException(status_code=404, detail="ShowTime not found")
    return updated

@showtime_router.delete("/{showtime_id}")
def delete_showtime(showtime_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return showtime_service.delete_showtime(db, showtime_id)
