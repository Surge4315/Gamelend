from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .. import models
from ..database import db_instance

router = APIRouter(tags=["Comments"])

get_db = db_instance.get_db


class CommentCreate(BaseModel):
    contents: str


@router.get("comments/{game_id}")
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


@router.post("comment/{game_id}")
def add_comment(
    game_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
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
