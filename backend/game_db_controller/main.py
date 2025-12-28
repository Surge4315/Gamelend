from fastapi import FastAPI, Depends, Query, HTTPException
from pydantic import BaseModel
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

#127.0.0.1:8000/
@app.get("/")
def root():
    return {"message": "Hello world"}

#127.0.0.1:8000/games?i=0
@app.get("/games")
def get_games(i: int = Query(0, description="ID gry od którego zaczynamy"), db: Session = Depends(get_db)):
    if i < 0:
        raise HTTPException(status_code=400, detail="invalid number, must be bigger or equal to 0")
    
    games = db.query(models.Game)\
              .filter(models.Game.id > (i)*18)\
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

#127.0.0.1:8000/games/1
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
#127.0.0.1:8000/comments/1
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
    
    
# Pydantic models
class CommentCreate(BaseModel):
    contents: str

@app.post("/comment/{game_id}")
def add_comment(game_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    # Sprawdzamy, czy gra istnieje
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Tworzymy nowy komentarz
    new_comment = models.Comment(game_id=game_id, contents=comment.contents)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "commentId": str(new_comment.id),
        "contents": new_comment.contents
    }
    
