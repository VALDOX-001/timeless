from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_seats
from Services import seat_service

seat_router = APIRouter(prefix="/seats", tags=["Seats"])

@seat_router.post("/", response_model=schemas.Seat)
def create_seat(seat: schemas.SeatCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return seat_service.create_seat(db, seat)

@seat_router.get("/", response_model=list[schemas.Seat])
def list_seats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return seat_service.get_seats(db, skip, limit)

@seat_router.get("/search", response_model=list[schemas.Seat])
def search_seats_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_seats(db=db, keyword=keyword, skip=skip, limit=limit)


@seat_router.get("/{seat_id}", response_model=schemas.SeatWithDetails)
def get_seat(seat_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    seat = seat_service.get_seat_by_id(db, seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat

@seat_router.put("/{seat_id}", response_model=schemas.Seat)
def update_seat(seat_id: int, seat_data: schemas.SeatUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = seat_service.update_seat(db, seat_id, seat_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Seat not found")
    return updated

@seat_router.delete("/{seat_id}")
def delete_seat(seat_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return seat_service.delete_seat(db, seat_id)
