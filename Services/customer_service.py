from sqlalchemy.orm import Session
from models import Customer
import traceback
import schemas

def create_customer(db: Session, customer_data: schemas.CustomerCreate):
    customer = Customer(**customer_data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Customer).offset(skip).limit(limit).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate):
    try:
        customer = get_customer_by_id(db, customer_id)
        if not customer:
            return None
        for key, value in customer_data.model_dump(exclude_unset=True).items():
            setattr(customer, key, value)
            db.commit()
            db.refresh(customer)
            return customer

    except Exception:
        traceback.print_exc()
        db.rollback()
        return None





def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return {"detail": "Customer not found"}
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted successfully"}