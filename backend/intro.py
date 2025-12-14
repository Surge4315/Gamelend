from fastapi import FastAPI, Depends, Query
from sqlalchemy import create_engine, text, Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
import enum
# ---------------------------------------------------------
# 1. Konfiguracja bazy
# ---------------------------------------------------------

user = "user_db"
password = "password_db"
host = "localhost"
port = "5432"
database = "game_db"

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------------------------------------------------
# 2. Model SQLAlchemy odpowiadający tabeli game
# ---------------------------------------------------------

class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)  # PostgreSQL Identity/Serial
    name = Column(String, nullable=False)
    image_link = Column(String)
    description = Column(String, nullable=False)
    studio = Column(String, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)
   
    categories = relationship("GameCategory", backref="game") 

class GameCategoriesEnum(str, enum.Enum):
    Action = "Action"
    Puzzle = "Puzzle"
    Adventure = "Adventure"
    Strategy = "Strategy"
    RPG = "RPG"
    FPS = "FPS"
    Sports = "Sports"
    Racing = "Racing"

# Model dla game_category
class GameCategory(Base):
    __tablename__ = "game_category"
    category = Column(Enum(GameCategoriesEnum), primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), primary_key=True)

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

#.../games?i=(numer_strony)
@app.get("/games")
def get_games(i: int = Query(0, description="ID gry od którego zaczynamy"), db: Session = Depends(get_db)):
    """
    Zwraca maksymalnie 18 gier, których ID jest większe od start_id
    """
    games = db.query(Game)\
              .filter(Game.id > (i-1)*18)\
              .order_by(Game.id)\
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
    
@app.get("/games/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        return {"error": "Game not found"}
    
    # Tworzymy listę kategorii
    categories = [gc.category.value for gc in game.categories]
    
    return {
        "gameId": game.id,
        "name": game.name,
        "cover": game.image_link,
        "studio": game.studio,
        "description": game.description,
        "categories": categories
    }


