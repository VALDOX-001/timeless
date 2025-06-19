from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import schemas
from database import get_db
from Services import playService

play_router = APIRouter(prefix="/plays", tags=["Plays"])


@play_router.post("/", response_model=schemas.Play)
def create_play(play: schemas.PlayCreate, db: Session = Depends(get_db)):
    return playService.create_play(db, play)


@play_router.get("/", response_model=List[schemas.Play])
def get_all_plays(
    skip: int = 0,
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None, description="Search plays by title or other fields"),
    db: Session = Depends(get_db)
):
    return playService.get_all_plays(db, skip=skip, limit=limit, search=search)


@play_router.get("/{play_id}", response_model=schemas.Play)
def get_play(play_id: int, db: Session = Depends(get_db)):
    play = playService.get_play_by_id(db, play_id)
    if not play:
        raise HTTPException(status_code=404, detail="Play not found")
    return play


@play_router.delete("/{play_id}", response_model=dict)
def delete_play(play_id: int, db: Session = Depends(get_db)):
    success = playService.delete_play(db, play_id)
    if not success:
        raise HTTPException(status_code=404, detail="Play not found or already deleted")
    return {"detail": "Play deleted successfully"}
