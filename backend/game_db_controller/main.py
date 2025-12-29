from fastapi import FastAPI, Depends, Query, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
import requests
import httpx
from .database import Database, Base
from . import models

db_instance = Database(
    user="user_db",
    password="password_db",
    host="localhost",
    port="5432",
    database="game_db",
)

engine = db_instance.engine
get_db = db_instance.get_db

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
    
    
# Pydantic model for comment creation
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
    
#functions that require communication between microservices    
BACKEND_USERS_URL = "http://127.0.0.1:8001"

@app.get("/my-borrows")
def my_borrows(email: str = Header(...), db: Session = Depends(get_db)):
    """
    Zwraca wszystkie gry aktualnie wypożyczone przez użytkownika na podstawie emaila,
    korzystając z endpointu /by-email w celu uzyskania UUID.
    """
    # Wywołanie lokalnego API /by-email
    try:
        response = httpx.get(f"{BACKEND_USERS_URL}/by-email", params={"email": email})
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(status_code=500, detail="Error calling /by-email endpoint")

    user_id = response.json()["id"]

    # Szukanie wypożyczeń po UUID użytkownika
    borrows = db.query(models.Borrow).filter(models.Borrow.user_id == user_id).all()

    result = []
    for b in borrows:
        copy = db.query(models.Copy).filter(models.Copy.copy_id == b.copy_id).first()
        if not copy:
            continue
        game = db.query(models.Game).filter(models.Game.id == copy.game_id).first()
        if not game:
            continue

        result.append({
            "copyId": b.copy_id,
            "gameId": game.id,
            "name": game.name,
            "cover": game.image_link,
            "borrowStartTime": b.borrow_start_time.isoformat()
        })

    return result