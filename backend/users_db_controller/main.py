from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import text
from uuid import UUID
from sqlalchemy.orm import Session
from .database import Database
from . import models

db_instance = Database(
    user="user_db",
    password="password_db",
    host="localhost",
    port="5433",
    database="users_db",
)

engine = db_instance.engine
get_db = db_instance.get_db



# Tworzenie tabel
models.Base.metadata.create_all(bind=engine)

# Wypisanie wersji PostgreSQL
with engine.connect() as connection:
    version = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", version.scalar())

app = FastAPI()

#127.0.0.1:8001/
@app.get("/")
def root():
    return {"message": "Hello world"}

#127.0.0.1:8001/user/{UUID}
@app.get("/user/{user_id}")
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Zwracamy dane użytkownika (bez haseł i tokenów)
    return {
        "id": str(user.id),
        "email": user.email,
        "provider": user.provider,
        "is_verified": user.is_verified,
        "pending_email": user.pending_email,
        "is_deletion_pending": user.is_deletion_pending,
        "deletion_scheduled_at": user.deletion_scheduled_at.isoformat() if user.deletion_scheduled_at else None,
        "roles": [role.role for role in user.roles]
    }


#127.0.0.1:8001/by-email
@app.get("/by-email")
def get_user_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    """
    Endpoint zwracający UUID użytkownika na podstawie podanego e-maila.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not fdound")
    
    return {"id": str(user.id)}


#127.0.0.1:8001/by-id
@app.get("/by-id")
def get_user_by_id(id: str = Query(...), db: Session = Depends(get_db)):
    """
    Endpoint zwracający email użytkownika na podstawie podanego UUID.
    """
    try:
        user_uuid = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
    
    user = db.query(models.User).filter(models.User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"email": user.email}

