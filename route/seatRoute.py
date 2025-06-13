from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import schemas
from services import seat_service

seat_router = APIRouter(prefix="/seats", tags=["Seats"])


@seat_router.post("/", response_model=schemas.Seat)
def create_seat(seat_data: schemas.SeatCreate, db: Session = Depends(get_db)):
    return seat_service.create_seat(db, seat_data)


@seat_router.get("/", response_model=List[schemas.Seat])
def get_all_seats(
    skip: int = 0,
    limit: int = Query(100, le=100),
    search: Optional[str] = Query(None, description="Search seats by criteria"),
    db: Session = Depends(get_db)
):
    return seat_service.get_all_seats(db, skip=skip, limit=limit, search=search)


@seat_router.get("/{seat_id}", response_model=schemas.Seat)
def get_seat(seat_id: int, db: Session = Depends(get_db)):
    seat = seat_service.get_seat_by_id(db, seat_id)
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat


@seat_router.put("/{seat_id}", response_model=schemas.Seat)
def update_seat(seat_id: int, seat_data: schemas.SeatUpdate, db: Session = Depends(get_db)):
    updated_seat = seat_service.update_seat(db, seat_id, seat_data)
    if updated_seat is None:
        raise HTTPException(status_code=404, detail="Seat not found or update failed")
    return updated_seat


@seat_router.delete("/{seat_id}", response_model=dict)
def delete_seat(seat_id: int, db: Session = Depends(get_db)):
    success = seat_service.delete_seat(db, seat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Seat not found or already deleted")
    return {"detail": "Seat deleted successfully"}
