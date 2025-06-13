from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import schemas
from services import ticket_service

ticket_router = APIRouter(prefix="/tickets", tags=["Tickets"])


@ticket_router.post("/", response_model=schemas.Ticket)
def create_ticket(ticket_data: schemas.TicketCreate, db: Session = Depends(get_db)):
    return ticket_service.create_ticket(db, ticket_data)


@ticket_router.get("/", response_model=List[schemas.Ticket])
def get_all_tickets(
    skip: int = 0,
    limit: int = Query(100, le=100),
    search: Optional[str] = Query(None, description="Search tickets by criteria"),
    db: Session = Depends(get_db)
):
    return ticket_service.get_all_tickets(db, skip=skip, limit=limit, search=search)


@ticket_router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = ticket_service.get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@ticket_router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(ticket_id: int, ticket_data: schemas.TicketUpdate, db: Session = Depends(get_db)):
    updated_ticket = ticket_service.update_ticket(db, ticket_id, ticket_data)
    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or update failed")
    return updated_ticket


@ticket_router.delete("/{ticket_id}", response_model=dict)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    deleted = ticket_service.delete_ticket(db, ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found or already deleted")
    return {"detail": "Ticket deleted successfully"}
