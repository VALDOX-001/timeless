from sqlalchemy.orm import Session
from models import Customer
import schemas


def create_customer(db: Session, customer_data: schemas.CustomerCreate):
    customer = Customer(
        name=customer_data.name,
        telephone=customer_data.telephone
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_all_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(db: Session, customer_id: int, customer_data: schemas.CustomerUpdate):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return None
    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer


def delete_customer(db: Session, customer_id: int):
    customer = get_customer_by_id(db, customer_id)
    if not customer:
        return False
    db.delete(customer)
    db.commit()
    return True