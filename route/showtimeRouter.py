from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import schemas
from Services import showtimeService

showtime_router = APIRouter(prefix="/showtimes", tags=["ShowTimes"])


@showtime_router.post("/", response_model=schemas.ShowTime)
def create_showtime(showtime: schemas.ShowTimeCreate, db: Session = Depends(get_db)):
    return showtimeService.create_showtime(db, showtime)


@showtime_router.get("/", response_model=List[schemas.ShowTime])
def get_all_showtimes(
    skip: int = 0,
    limit: int = Query(100, le=100),
    search: Optional[str] = Query(None, description="Search showtimes by criteria"),
    db: Session = Depends(get_db)
):
    return showtimeService.get_all_showtimes(db, skip=skip, limit=limit, search=search)


@showtime_router.get("/{showtime_id}", response_model=schemas.ShowTime)
def get_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime = showtimeService.get_showtime_by_id(db, showtime_id)
    if not showtime:
        raise HTTPException(status_code=404, detail="ShowTime not found")
    return showtime


@showtime_router.put("/{showtime_id}", response_model=schemas.ShowTime)
def update_showtime(showtime_id: int, showtime_data: schemas.ShowTimeUpdate, db: Session = Depends(get_db)):
    updated = showtimeService.update_showtime(db, showtime_id, showtime_data)
    if not updated:
        raise HTTPException(status_code=404, detail="ShowTime not found or update failed")
    return updated


@showtime_router.delete("/{showtime_id}", response_model=dict)
def delete_showtime(showtime_id: int, db: Session = Depends(get_db)):
    deleted = showtimeService.delete_showtime(db, showtime_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ShowTime not found or already deleted")
    return {"detail": "ShowTime deleted successfully"}
