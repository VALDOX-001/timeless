from sqlalchemy.orm import Session
from sqlalchemy import or_, String
from models import Actor, Director, Play, Ticket, Seat, Customer, ShowTime, Price


# 🎭 Search Actors
def search_actors(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Actor).filter(
        or_(
            Actor.name.ilike(f"%{keyword}%"),
            Actor.gender.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 🎬 Search Directors
def search_directors(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Director).filter(
        or_(
            Director.name.ilike(f"%{keyword}%"),
            Director.citizenship.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 📚 Search Plays
def search_plays(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Play).filter(
        or_(
            Play.title.ilike(f"%{keyword}%"),
            Play.genre.ilike(f"%{keyword}%"),
            Play.synopsis.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 🎟️ Search Tickets
def search_tickets(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Ticket).join(Customer).join(ShowTime).filter(
        or_(
            Ticket.TicketNo.ilike(f"%{keyword}%"),
            Customer.name.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 🪑 Search Seats
def search_seats(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Seat).filter(
        or_(
            Seat.row_number.cast(String).ilike(f"%{keyword}%"),
            Seat.seat_number.cast(String).ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 👤 Search Customers
def search_customers(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Customer).filter(
        or_(
            Customer.name.ilike(f"%{keyword}%"),
            Customer.gender.ilike(f"%{keyword}%"),
            Customer.email.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# ⏰ Search ShowTimes
def search_showtimes(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(ShowTime).join(Play).filter(
        or_(
            Play.title.ilike(f"%{keyword}%"),
            Play.genre.ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()


# 💰 Search Prices
def search_prices(db: Session, keyword: str = "", skip: int = 0, limit: int = 10):
    return db.query(Price).filter(
        or_(
            Price.category.ilike(f"%{keyword}%"),
            Price.amount.cast(String).ilike(f"%{keyword}%")
        )
    ).offset(skip).limit(limit).all()
