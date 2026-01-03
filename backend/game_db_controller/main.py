from fastapi import FastAPI
from sqlalchemy import text
from .database import db_instance
from . import models
from .routers import games, comments, borrows

engine = db_instance.engine

# tworzenie tabel
models.Base.metadata.create_all(bind=engine)

# wypisanie wersji PostgreSQL
with engine.connect() as connection:
    version = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", version.scalar())

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world"}

# rejestracja routerów
app.include_router(games.router)
app.include_router(comments.router)
app.include_router(borrows.router)
