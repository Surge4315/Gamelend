from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import httpx
from .. import models
from ..database import db_instance

router = APIRouter(tags=["Borrows"])

get_db = db_instance.get_db

BACKEND_USERS_URL = "http://127.0.0.1:8001"


@router.get("/my-borrows")
def my_borrows(
    email: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        response = httpx.get(
            f"{BACKEND_USERS_URL}/by-email",
            params={"email": email}
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail="User service error")

    user_id = response.json()["id"]

    borrows = db.query(models.Borrow).filter(
        models.Borrow.user_id == user_id
    ).all()

    result = []
    for b in borrows:
        copy = db.query(models.Copy).filter(
            models.Copy.copy_id == b.copy_id
        ).first()
        if not copy:
            continue

        game = db.query(models.Game).filter(
            models.Game.id == copy.game_id
        ).first()
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
