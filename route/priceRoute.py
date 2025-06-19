from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
import schemas
from Services import price_services

price_router = APIRouter(prefix="/prices", tags=["Prices"])


@price_router.post("/", response_model=schemas.Price)
def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db)):
    return price_services.create_price(db, price)


@price_router.get("/", response_model=List[schemas.Price])
def list_prices(
    skip: int = 0,
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search prices by relevant fields"),
    db: Session = Depends(get_db)
):
    return price_services.get_prices(db=db, skip=skip, limit=limit, search=search)


@price_router.get("/{price_id}", response_model=schemas.Price)
def get_price(price_id: int, db: Session = Depends(get_db)):
    price = price_services.get_price_by_id(db, price_id)
    if not price:
        raise HTTPException(status_code=404, detail="Price not found")
    return price


@price_router.put("/{price_id}", response_model=schemas.Price)
def update_price(price_id: int, price_data: schemas.PriceUpdate, db: Session = Depends(get_db)):
    updated_price = price_services.update_price(db, price_id, price_data)
    if not updated_price:
        raise HTTPException(status_code=404, detail="Price not found or update failed")
    return updated_price


@price_router.delete("/{price_id}", response_model=dict)
def delete_price(price_id: int, db: Session = Depends(get_db)):
    success = price_services.delete_price(db, price_id)
    if not success:
        raise HTTPException(status_code=404, detail="Price not found or already deleted")
    return {"detail": "Price deleted successfully"}
