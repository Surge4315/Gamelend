from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class Database:
    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        
        self.DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Create a single database instance
db_instance = Database(
    user="user_db",
    password="password_db",
    host="localhost",
    port="5432",
    database="game_db",
)
