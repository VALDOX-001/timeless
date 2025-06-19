from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_tickets
from Services import ticket_service

ticket_router = APIRouter(prefix="/tickets", tags=["Tickets"])

@ticket_router.post("/", response_model=schemas.Ticket)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return ticket_service.create_ticket(db, ticket)

@ticket_router.get("/", response_model=list[schemas.Ticket])
def list_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return ticket_service.get_tickets(db, skip, limit)

@ticket_router.get("/search", response_model=list[schemas.Ticket])
def search_ticket_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_tickets(db=db, keyword=keyword, skip=skip, limit=limit)

@ticket_router.get("/{ticket_id}", response_model=schemas.TicketWithDetails)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    ticket = ticket_service.get_ticket_by_id(db, ticket_id)
    if not ticket: raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@ticket_router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(ticket_id: int, ticket_data: schemas.TicketUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = ticket_service.update_ticket(db, ticket_id, ticket_data)
    if not updated: raise HTTPException(status_code=404, detail="Ticket not found")
    return updated

@ticket_router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return ticket_service.delete_ticket(db, ticket_id)
