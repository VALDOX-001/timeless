from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
import schemas
from Services import actor_services

actor_router = APIRouter(prefix="/actors", tags=["Actors"])


@actor_router.post("/", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    return actor_services.create_actor(db, actor)


@actor_router.get("/", response_model=schemas.PaginatedActors)
def list_actors(
    skip: int = 0,
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search actors by name"),
    db: Session = Depends(get_db)
):
    actors, total = actor_services.get_actors(db, skip=skip, limit=limit, search=search)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": actors
    }


@actor_router.get("/{actor_id}", response_model=schemas.ActorWithRelationships)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = actor_services.get_actor_by_id(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor


@actor_router.put("/{actor_id}", response_model=schemas.Actor)
def update_actor(actor_id: int, actor_data: schemas.ActorUpdate, db: Session = Depends(get_db)):
    updated_actor = actor_services.update_actor(db, actor_id, actor_data)
    if not updated_actor:
        raise HTTPException(status_code=404, detail="Actor not found or update failed")
    return updated_actor


@actor_router.delete("/{actor_id}", response_model=dict)
def delete_actor(actor_id: int, db: Session = Depends(get_db)):
    success = actor_services.delete_actor(db, actor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Actor not found or already deleted")
    return {"detail": "Actor deleted successfully"}
