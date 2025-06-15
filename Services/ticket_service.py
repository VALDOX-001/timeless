from sqlalchemy.orm import Session
from models import Ticket
import traceback
import schemas

def create_ticket(db: Session, ticket_data: schemas.TicketCreate):
    ticket = Ticket(**ticket_data.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_tickets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket_data: schemas.TicketUpdate):
    try:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            return None
        for key, value in ticket_data.model_dump(exclude_unset=True).items():
            setattr(ticket, key, value)
            db.commit()
            db.refresh(ticket)
            return ticket
    except Exception:
        traceback.print_exc()
        db.rollback()
        return None

def delete_ticket(db: Session, ticket_id: int):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return {"detail": "Ticket not found"}
    db.delete(ticket)
    db.commit()
    return {"detail": "Ticket deleted successfully"}