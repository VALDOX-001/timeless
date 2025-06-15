from sqlalchemy.orm import Session
from models import Ticket
import schemas  # consistent with the rest of your code

def create_ticket(db: Session, ticket_data: schemas.TicketCreate):
    ticket = Ticket(
        seat_id=ticket_data.seat_id,
        show_time_id=ticket_data.show_time_id,
        customer_id=ticket_data.customer_id
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_all_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket_data: schemas.TicketUpdate):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    for key, value in ticket_data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket

def delete_ticket(db: Session, ticket_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return False
    db.delete(ticket)
    db.commit()
    return True
