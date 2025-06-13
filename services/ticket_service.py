from sqlalchemy.orm import Session
from models import Ticket
import schema

def create_ticket(db: Session, ticket_data: schema.TicketCreate):
    ticket = Ticket(
        seat_id=ticket_data.Seat_SeatNo[0],  # example logic
        show_time_id=ticket_data.ShowTime_Play_PlayId,
        customer_id=ticket_data.Customer_CustomerId
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def get_all_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ticket).offset(skip).limit(limit).all()

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()

def update_ticket(db: Session, ticket_id: int, ticket_data: schema.TicketUpdate):
    ticket = get_ticket_by_id(db, ticket_id)
    if not ticket:
        return None
    if ticket_data.TicketNo is not None:
        # Just a placeholder for a field (depends on your real DB model)
        pass
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
