#obsolete but for reference exists
import jwt
import uuid
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"

def create_access_token(user_id: str, roles, expires_in_minutes: int = 15) -> str:
    # Zamiana user_id na UUID, jeśli nie jest UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError("Niepoprawny format UUID dla user_id")

    payload = {
        "sub": str(user_uuid),
        "roles": roles,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)).timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print("Generated JWT Token:")
    print(token)
    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token wygasł")
    except jwt.InvalidTokenError:
        raise ValueError("Nieprawidłowy token")

if __name__ == "__main__":
    # Przykładowe wywołanie z argumentami
    token = create_access_token(
        user_id="550e8400-e29b-41d4-a716-446655440000",
        roles=["ADMIN"],
        expires_in_minutes=30
    )
    
    decoded = decode_access_token(token)
    print("\nDecoded JWT Payload:")
    print(decoded)
