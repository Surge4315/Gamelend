from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import db_instance

router = APIRouter(prefix="/games", tags=["Games"])

get_db = db_instance.get_db


@router.get("")
def get_games(
    i: int = Query(0, description="ID gry od którego zaczynamy"),
    db: Session = Depends(get_db)
):
    if i < 0:
        raise HTTPException(status_code=400, detail="invalid number")

    games = (
        db.query(models.Game)
        .filter(models.Game.id > i * 18)
        .order_by(models.Game.id)
        .limit(18)
        .all()
    )

    return [
        {
            "gameId": g.id,
            "name": g.name,
            "cover": g.image_link,
        }
        for g in games
    ]


@router.get("/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return {
        "gameId": game.id,
        "name": game.name,
        "cover": game.image_link,
        "studio": game.studio,
        "description": game.description,
        "categories": [gc.category.value for gc in game.game_categories],
    }
