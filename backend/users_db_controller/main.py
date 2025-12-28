from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import text
from uuid import UUID
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

#127.0.0.1:8001/
@app.get("/")
def root():
    return {"message": "Hello world"}

#127.0.0.1:8001/user/UUID
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

