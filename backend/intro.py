from sqlalchemy import create_engine, text
from fastapi import FastAPI, Depends

# Parametry połączenia
user = "auth_user"
password = "auth_password"
host = "localhost"
port = "5432"
database = "auth_db"

# Tworzenie silnika SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# Przykładowe użycie połączenia
with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))
    for row in result:
        print(row[0])
        
app = FastAPI()

#gotta start somewhere
@app.get("/")
def root():
    return {"message": "Hello world"}