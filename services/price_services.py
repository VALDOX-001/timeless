from sqlalchemy.orm import Session
from models import Price
import schemas

def create_price(db: Session, price_data: schemas.PriceCreate):
    prices = Price(
        seat_id=price_data.seat_id,
        show_time_id=price_data.show_time_id,
        price=price_data.price
    )
    db.add(prices)
    db.commit()
    db.refresh(prices)
    return prices

def get_prices(skip: int, limit: int, db: Session):
    return db.query(Price).offset(skip).limit(limit).all()

def get_price_by_id(db: Session, price_id: int):
    return db.query(Price).filter(Price.id == price_id).first()

def update_price(db: Session, price_id: int, price_data: schemas.PriceUpdate):
    price = get_price_by_id(db, price_id)
    if not price:
        return None
    for key, value in price_data.model_dump():
        setattr(price, key, value)
    db.commit()
    db.refresh(price)
    return price

def delete_price(db: Session, price_id: int):
    price = get_price_by_id(db, price_id)
    if not price:
        return {"detail": "Price not found"}
    db.delete(price)
    db.commit()
    return {"detail": "Price deleted successfully"}
