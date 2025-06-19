from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_customers
from Services import customer_service

customer_router = APIRouter(prefix="/customers", tags=["Customers"])

@customer_router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return customer_service.create_customer(db, customer)

@customer_router.get("/", response_model=list[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return customer_service.get_customers(db, skip, limit)

@customer_router.get("/search", response_model=list[schemas.Customer])
def search_customers_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_customers(db=db, keyword=keyword, skip=skip, limit=limit)

@customer_router.get("/{customer_id}", response_model=schemas.CustomerWithTickets)
def get_customer(customer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    customer = customer_service.get_customer_by_id(db, customer_id)
    if not customer: raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@customer_router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer_data: schemas.CustomerUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = customer_service.update_customer(db, customer_id, customer_data)
    if not updated: raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@customer_router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return customer_service.delete_customer(db, customer_id)
