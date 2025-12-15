from fastapi import FastAPI, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models

# Tworzenie tabel
Base.metadata.create_all(bind=engine)

# Wypisanie wersji PostgreSQL
with engine.connect() as connection:
    version = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", version.scalar())

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world"}

@app.get("/games")
def get_games(i: int = Query(0, description="ID gry od którego zaczynamy"), db: Session = Depends(get_db)):
    games = db.query(models.Game)\
              .filter(models.Game.id > (i-1)*18)\
              .order_by(models.Game.id)\
              .limit(18)\
              .all()
    return [
        {
            "gameId": g.id,
            "name": g.name,
            "cover": g.image_link,
        }
        for g in games
    ]

@app.get("/games/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        return {"error": "Game not found"}
    
    categories = [gc.category.value for gc in game.game_categories]
    return {
        "gameId": game.id,
        "name": game.name,
        "cover": game.image_link,
        "studio": game.studio,
        "description": game.description,
        "categories": categories
    }

@app.get("/comments/{game_id}")
def get_comments(game_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.game_id == game_id).all()
    return [
        {
            "commentId": str(c.id),
            "contents": c.contents
        }
        for c in comments
    ]
