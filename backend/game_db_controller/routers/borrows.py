from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel, EmailStr
from uuid import UUID
import httpx
from .. import models
from ..database import db_instance

router = APIRouter(tags=["Borrows"])

get_db = db_instance.get_db

BACKEND_USERS_URL = "http://127.0.0.1:8001"


def verify_user_email(email: str) -> str:
    """
    Weryfikuje email użytkownika i zwraca jego ID.
    
    Args:
        email: Adres email użytkownika
        
    Returns:
        str: ID użytkownika
        
    Raises:
        HTTPException: Gdy użytkownik nie istnieje (404) lub wystąpił błąd serwisu (500)
    """
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
    
    return response.json()["id"]


@router.get("/my-borrows")
def my_borrows(
    email: str = Header(...),
    db: Session = Depends(get_db)
):
    user_id = verify_user_email(email)

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


class LendRequest(BaseModel):
    copyId: UUID
    email: EmailStr

@router.post("/lend", status_code=201)
def lend_game(
    data: LendRequest,
    db: Session = Depends(get_db)
):
    # walidacja copyId + race condition handling
    copy = (
    db.query(models.Copy)
    .with_for_update()
    .filter(models.Copy.copy_id == data.copyId)
    .first()
)

    if not copy:
        raise HTTPException(
            status_code=404,
            detail="Copy with given copyId does not exist"
        )

    if not copy.available:
        raise HTTPException(
            status_code=400,
            detail="This copy is already borrowed"
        )

    # pobranie userId po emailu
    user_id = verify_user_email(data.email)

    # zapis wypożyczenia + update copy
    borrow = models.Borrow(
        user_id=user_id,
        copy_id=copy.copy_id
    )

    try:
        db.add(borrow)
        copy.available = False  # trigger zajmie się game.available_copies
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This user already borrowed this copy"
        )

    return {
        "message": "Game copy successfully lent",
        "copyId": copy.copy_id,
        "userId": user_id
    }


class ReceiveRequest(BaseModel):
    copyId: UUID
    email: EmailStr

@router.delete("/receive", status_code=200)
def receive_game(
    data: ReceiveRequest,
    db: Session = Depends(get_db)
):
    # pobranie userId po emailu
    user_id = verify_user_email(data.email)

    # blokada kopii (race-condition!)
    copy = (
        db.query(models.Copy)
        .with_for_update()
        .filter(models.Copy.copy_id == data.copyId)
        .first()
    )

    if not copy:
        raise HTTPException(
            status_code=404,
            detail="Copy with given copyId does not exist"
        )

    # sprawdzenie czy istnieje wypożyczenie
    borrow = db.query(models.Borrow).filter(
        models.Borrow.copy_id == data.copyId,
        models.Borrow.user_id == user_id
    ).first()

    if not borrow:
        raise HTTPException(
            status_code=404,
            detail="This copy is not borrowed by this user"
        )

    # usunięcie wypożyczenia + zwrot kopii
    db.delete(borrow)
    copy.available = True  # trigger zwiększy game.available_copies
    db.commit()

    return {
        "message": "Game copy successfully returned",
        "copyId": copy.copy_id,
        "userId": user_id
    }
    
def get_user_email_by_id(user_id: str) -> str:
   
    # Pobiera email użytkownika na podstawie jego ID.

    try:
        response = httpx.get(
            f"{BACKEND_USERS_URL}/by-id",
            params={"id": user_id}
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail="User service error")
    
    return response.json()["email"]    
    
#wszystkie wypożyczenia    
@router.get("/borrows")
def get_all_borrows(
    i: int = Query(0, description="Numer strony (każda strona to 18 wypożyczeń)"),
    db: Session = Depends(get_db)
):
    """
    Endpoint admina do pobierania wszystkich aktywnych wypożyczeń.
    Zwraca wypożyczenia posortowane od najstarszych, paginowane po 18 elementów.
    """
    if i < 0:
        raise HTTPException(status_code=400, detail="Invalid page number")
    
    borrows = (
        db.query(models.Borrow)
        .order_by(models.Borrow.borrow_start_time)
        .offset(i * 18)
        .limit(18)
        .all()
    )
    
    result = []
    for b in borrows:
        # Pobierz email użytkownika
        try:
            user_email = get_user_email_by_id(b.user_id)
        except HTTPException:
            continue  # Pomiń jeśli użytkownik nie istnieje
        
        # Pobierz kopię gry
        copy = db.query(models.Copy).filter(
            models.Copy.copy_id == b.copy_id
        ).first()
        if not copy:
            continue
        
        # Pobierz grę dla obrazka okładki
        game = db.query(models.Game).filter(
            models.Game.id == copy.game_id
        ).first()
        if not game:
            continue
        
        result.append({
            "email": user_email,
            "copyId": b.copy_id,
            "borrowStartTime": b.borrow_start_time.isoformat(),
            "cover": game.image_link
        })
    
    return result

#email
@router.get("/borrows/by-email")
def get_borrows_by_email(
    email: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint admina do pobierania wszystkich wypożyczeń konkretnego użytkownika.
    Wymaga podania emailu użytkownika.
    Sortuje od najstarszych wypożyczeń.
    """
    user_id = verify_user_email(email)
    
    borrows = (
        db.query(models.Borrow)
        .filter(models.Borrow.user_id == user_id)
        .order_by(models.Borrow.borrow_start_time)
        .all()
    )
    
    result = []
    for b in borrows:
        # Pobierz email użytkownika
        try:
            user_email = get_user_email_by_id(b.user_id)
        except HTTPException:
            continue  # Pomiń jeśli użytkownik nie istnieje
        
        # Pobierz kopię gry
        copy = db.query(models.Copy).filter(
            models.Copy.copy_id == b.copy_id
        ).first()
        if not copy:
            continue
        
        # Pobierz grę dla obrazka okładki
        game = db.query(models.Game).filter(
            models.Game.id == copy.game_id
        ).first()
        if not game:
            continue
        
        result.append({
            "email": user_email,
            "copyId": b.copy_id,
            "borrowStartTime": b.borrow_start_time.isoformat(),
            "cover": game.image_link
        })
    
    return result
    
    
    