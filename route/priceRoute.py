from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_prices
from Services import price_services

price_router = APIRouter(prefix="/prices", tags=["Prices"])

@price_router.post("/", response_model=schemas.Price)
def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return price_services.create_price(db, price)

@price_router.get("/", response_model=list[schemas.Price])
def list_prices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return price_services.get_prices(db, skip, limit)

@price_router.get("/search", response_model=list[schemas.Price])
def search_prices_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_prices(db=db, keyword=keyword, skip=skip, limit=limit)

@price_router.get("/{price_id}", response_model=schemas.PriceWithDetails)
def get_price(price_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    price = price_services.get_price_by_id(db, price_id)
    if not price: raise HTTPException(status_code=404, detail="Price not found")
    return price

@price_router.put("/{price_id}", response_model=schemas.Price)
def update_price(price_id: int, price_data: schemas.PriceUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = price_services.update_price(db, price_id, price_data)
    if not updated: raise HTTPException(status_code=404, detail="Price not found")
    return updated

@price_router.delete("/{price_id}")
def delete_price(price_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return price_services.delete_price(db, price_id)
