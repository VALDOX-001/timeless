
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_actors
from Services import actor_services


actor_router = APIRouter(prefix="/actors", tags=["Actors"])


@actor_router.post("/", response_model=schemas.Actor)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return actor_services.create_actor(db, actor)

@actor_router.get("/", response_model=list[schemas.Actor])
def list_actors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return actor_services.get_actors(db, skip, limit)

@actor_router.get("/search", response_model=list[schemas.Actor])
def search_actor_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_actors(db=db, keyword=keyword, skip=skip, limit=limit)

@actor_router.get("/{actor_id}", response_model=schemas.ActorWithPlays)
def get_actor(actor_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    actor = actor_services.get_actor_by_id(db, actor_id)
    if not actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return actor

@actor_router.put("/{actor_id}", response_model=schemas.Actor)
def update_actor(actor_id: int, actor_data: schemas.ActorUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = actor_services.update_actor(db, actor_id, actor_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Actor not found")
    return updated

@actor_router.delete("/{actor_id}")
def delete_actor(actor_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return actor_services.delete_actor(db, actor_id)
