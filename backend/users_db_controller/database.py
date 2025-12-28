from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

user = "user_db"
password = "password_db"
host = "localhost"
port = "5433"
database = "users_db"

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
