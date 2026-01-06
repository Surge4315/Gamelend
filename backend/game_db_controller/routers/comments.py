from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .. import models
from ..database import db_instance
from ..jwt_decoder import decode_access_token
import requests

router = APIRouter(tags=["Comments"])

get_db = db_instance.get_db


class CommentCreate(BaseModel):
    contents: str


@router.get("/comments/{game_id}")
def get_comments(game_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(
        models.Comment.game_id == game_id
    ).all()

    return [
        {
            "commentId": str(c.id),
            "contents": c.contents
        }
        for c in comments
    ]


@router.post("/comment/{game_id}")
def add_comment(
    game_id: int,
    comment: CommentCreate,
    token: str = Header(...),
    db: Session = Depends(get_db)
):
    # Dekodowanie JWT i wyciągnięcie user_id
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    # Weryfikacja użytkownika przez endpoint by-id-id
    try:
        response = requests.get(
            "http://127.0.0.1:8001/by-id-id",
            params={"id": user_id}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="User service unavailable")
    
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    new_comment = models.Comment(
        game_id=game_id,
        contents=comment.contents
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "commentId": str(new_comment.id),
        "contents": new_comment.contents
    }
