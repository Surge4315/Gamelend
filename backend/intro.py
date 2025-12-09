from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, String, Integer
import uuid

# ---------------------------------------------------------
# 1. Konfiguracja bazy
# ---------------------------------------------------------

user = "auth_user"
password = "auth_password"
host = "localhost"
port = "5432"
database = "auth_db"

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------------------------------------------------
# 2. Model SQLAlchemy odpowiadający tabeli game
# ---------------------------------------------------------

class Game(Base):
    __tablename__ = "game"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    image_link = Column(String)
    description = Column(String, nullable=False)
    studio = Column(String, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)

# Tworzenie tabel, jeśli nie istnieją
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# 3. FastAPI + DB dependency
# ---------------------------------------------------------

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# 4. Wypisanie SELECT version() przy starcie
# ---------------------------------------------------------

with engine.connect() as connection:
    version = connection.execute(text("SELECT version();"))
    print("PostgreSQL version:", version.scalar())


# ---------------------------------------------------------
# 5. Endpointy
# ---------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/games")
def get_games(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    return [
        {
            "gameId": g.id,
            "name": g.name,
            "cover": g.image_link,
            "description": g.description,
            "studio": g.studio,
            "availableCopies": g.available_copies
        }
        for g in games
    ]
    

