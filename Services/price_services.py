from sqlalchemy.orm import Session
from models import Price
import traceback
import schemas

def create_price(db: Session, price_data: schemas.PriceCreate):
    price = Price(**price_data.model_dump())
    db.add(price)
    db.commit()
    db.refresh(price)
    return price

def get_prices(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Price).offset(skip).limit(limit).all()

def get_price_by_id(db: Session, price_id: int):
    return db.query(Price).filter(Price.id == price_id).first()

def update_price(db: Session, price_id: int, price_data: schemas.PriceUpdate):
    try:
        price = get_price_by_id(db, price_id)
        if not price:
            return None
        for key, value in price_data.model_dump(exclude_unset=True).items():
            setattr(price, key, value)
            db.commit()
            db.refresh(price)
            return price
    except Exception:
        traceback.print_exc()
        db.rollback()
        return None
<<<<<<< HEAD:Services/price_services.py

=======
    for key, value in price_data.model_dump().items():
        setattr(price, key, value)
    db.commit()
    db.refresh(price)
    return price
>>>>>>> e038b47b3e33613ad5f25374d83882acc461646c:services/price_services.py

def delete_price(db: Session, price_id: int):
    price = get_price_by_id(db, price_id)
    if not price:
        return {"detail": "Price not found"}
    db.delete(price)
    db.commit()
    return {"detail": "Price deleted successfully"}