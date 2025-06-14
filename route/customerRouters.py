from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
from database import get_db
from Services import customerService

customer_router = APIRouter(prefix="/customers", tags=["Customers"])


@customer_router.post("/", response_model=schemas.Customer)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return customerService.create_customer(db, customer)


@customer_router.get("/", response_model=List[schemas.Customer])
def get_all_customers(
    skip: int = 0,
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search customers by name or email"),
    db: Session = Depends(get_db)
):
    return customerService.get_all_customers(db, skip=skip, limit=limit, search=search)


@customer_router.get("/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customerService.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@customer_router.delete("/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    success = customerService.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found or already deleted")
    return {"detail": "Customer deleted successfully"}
