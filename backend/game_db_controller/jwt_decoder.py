import jwt
import uuid
from datetime import datetime, timedelta, timezone

SECRET_KEY = "amogus"
ALGORITHM = "HS256"

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token wygasł")
    except jwt.InvalidTokenError:
        raise ValueError("Nieprawidłowy token")