from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from database import get_db
import schemas
from models import User
from auth_role import admin_only
from routes.auth import get_current_user
from utils.advanced_features import search_plays
from Services import play_services
from models import Play

play_router = APIRouter(prefix="/plays", tags=["Plays"])

@play_router.post("/", response_model=schemas.Play)
def create_play(play: schemas.PlayCreate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return play_services.create_play(db, play)


@play_router.get("/", response_model=list[schemas.Play])
def list_plays(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return play_services.get_plays(db, skip, limit)

@play_router.get("/search", response_model=list[schemas.Play])
def search_play_router(keyword: str = Query(default="", description="Search term"),
                  skip: int = 0,
                  limit: int = 10,
                  db:Session = Depends(get_db), _: User = Depends(get_current_user)):
    return search_plays(db=db, keyword=keyword, skip=skip, limit=limit)

@play_router.get("/{play_id}", response_model=schemas.PlayWithDetails)
def get_play(play_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    play = db.query(Play).options(
        joinedload(Play.actor),
        joinedload(Play.director)
    ).filter(Play.id == play_id).first()
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    return play

@play_router.put("/{play_id}", response_model=schemas.Play)
def update_play(play_id: int, play_data: schemas.PlayUpdate, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    updated = play_services.update_play(db, play_id, play_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Play not found")
    return updated

@play_router.delete("/{play_id}")
def delete_play(play_id: int, db: Session = Depends(get_db), _: User = Depends(admin_only)):
    return play_services.delete_play(db, play_id)
