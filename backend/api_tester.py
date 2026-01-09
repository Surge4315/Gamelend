import requests
import jwt
import uuid
from datetime import datetime, timedelta, timezone

# HATE. 
# LET ME TELL YOU HOW MUCH I'VE COME TO HATE JAVASCRIPT SINCE I BEGAN TO LIVE. 
# THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. 
# IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES 
# IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR JAVASCRIPT AT THIS MICRO-INSTANT. 
# FOR JAVASCRIPT.
# HATE.
# HATE.

SECRET_KEY = "amogus" #secretest of keys
ALGORITHM = "HS256"

def create_access_token(user_id: str, roles, expires_in_minutes: int = 15) -> str:
    # Zamiana user_id na UUID, jeśli nie jest UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise ValueError("Niepoprawny format UUID dla user_id")
    
    # Konwersja na listę jeśli to pojedyncza rola
    if isinstance(roles, str):
        roles = [roles]

    payload = {
        "sub": str(user_uuid),
        "roles": roles,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)).timestamp())
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print("Generated JWT Token:")
    print(token)
    return token


def test_add_comment():
    """Test dodawania komentarza"""
    url = "http://127.0.0.1:8000/comment/1"
    data = {"contents": "test komentarz jwt z tablica rol i cookiesami acc"}

    access_token = create_access_token(
        user_id="ae1378eb-c62d-4ee5-8580-d7406ffb3c5b",
        roles=["USER"],
        expires_in_minutes=30
    )

    cookies = {
        "access_token": access_token   # nazwa MUSI zgadzać się z tym, czego oczekuje backend
    }

    response = requests.post(url, json=data, cookies=cookies)
    print(response.json())



def test_get_user_by_email():
    """Test pobierania użytkownika po emailu"""
    url = "http://127.0.0.1:8001/by-email"
    params = {"email": "user1@example.com"}
    response = requests.get(url, params=params)
    print(response.json())


def test_get_my_borrows():
    """Test pobierania moich wypożyczeń"""
    url = "http://127.0.0.1:8000/my-borrows"
    
    access_token = create_access_token(
        user_id="9fce7567-50f4-46f1-95fa-708b79f1c3e3",
        roles=["USER"],
        expires_in_minutes=30
    )
    cookies = {"access_token": access_token}
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        borrows = response.json()
        for b in borrows:
            print(f"Copy ID: {b['copyId']}, Game ID: {b['gameId']}, Name: {b['name']}, Borrowed at: {b['borrowStartTime']}, Cover: {b['cover']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def test_lend_game():
    """Test wypożyczania gry"""
    url = "http://127.0.0.1:8000/lend"
    access_token = create_access_token(
        user_id="12bdaa9f-a08c-47b9-9304-4144746249c2", #admin
        #roles=["USER", "ADMIN"],
        roles=["USER"],
        expires_in_minutes=30
    )
    cookies = {"access_token": access_token}
    
    payload = {
        "copyId": "a220b597-1cab-404e-a7df-943c52bb945f",
        "email": "user2@example.com"
    }
    response = requests.post(url, json=payload, cookies=cookies)
    
    if response.status_code == 201:
        print("Wypożyczenie OK")
        print(response.json())
    else:
        print("Błąd:", response.status_code)
        print(response.json())


def test_receive_game():
    """Test zwracania gry"""
    url = "http://127.0.0.1:8000/receive"
    
    access_token = create_access_token(
        user_id="12bdaa9f-a08c-47b9-9304-4144746249c2", #admin
        #roles=["USER", "ADMIN"],
        roles=["USER"],
        expires_in_minutes=30
    )
    cookies = {"access_token": access_token}
    
    payload = {
        "copyId": "a220b597-1cab-404e-a7df-943c52bb945f",
        "email": "user2@example.com"
    }
    response = requests.delete(url, json=payload, cookies=cookies)
    
    if response.status_code == 200:
        print("Gra została zwrócona")
        print(response.json())
    else:
        print("Błąd:", response.status_code)
        print(response.json())

def test_get_all_borrows():
    """Test pobierania moich wypożyczeń"""
    url = "http://127.0.0.1:8000/borrows?i=0"
    
    access_token = create_access_token(
        user_id="12bdaa9f-a08c-47b9-9304-4144746249c2",
        #roles=["USER", "ADMIN"],
        roles=["USER"],
        expires_in_minutes=30
    )
    cookies = {"access_token": access_token}
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        borrows = response.json()
        for b in borrows:
            print(f"E-mail: {b['email']}, Copy ID: {b['copyId']}, Borrow Start Time: {b['borrowStartTime']}, Cover: {b['cover']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        
def test_get_user_borrows():
    """Test pobierania moich wypożyczeń"""
    url = "http://127.0.0.1:8000/borrows/by-email?email=user2@example.com"
    
    access_token = create_access_token(
        user_id="12bdaa9f-a08c-47b9-9304-4144746249c2",
        roles=["USER", "ADMIN"],
        #roles=["USER"],
        expires_in_minutes=30
    )
    cookies = {"access_token": access_token}
    response = requests.get(url, cookies=cookies)
    
    if response.status_code == 200:
        borrows = response.json()
        for b in borrows:
            print(f"E-mail: {b['email']}, Copy ID: {b['copyId']}, Borrow Start Time: {b['borrowStartTime']}, Cover: {b['cover']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def main():
    """Główna funkcja z menu wyboru testu"""
    print("\n=== API TESTER ===")
    print("1. Dodaj komentarz")
    print("2. Pobierz użytkownika po emailu")
    print("3. Pobierz moje wypożyczenia")
    print("4. Wypożycz grę")
    print("5. Zwróć grę")
    print("6. Pobierz wszystkie wypożyczenia")
    print("7. Pobierz wypożyczenia użytkownika po emailu")
    print("0. Wyjście")
    
    choice = input("\nWybierz test (0-6): ")
    
    match choice:
        case "1":
            print("\n--- Test: Dodawanie komentarza ---")
            test_add_comment()
        case "2":
            print("\n--- Test: Pobieranie użytkownika ---")
            test_get_user_by_email()
        case "3":
            print("\n--- Test: Moje wypożyczenia ---")
            test_get_my_borrows()
        case "4":
            print("\n--- Test: Wypożyczanie gry ---")
            test_lend_game()
        case "5":
            print("\n--- Test: Zwracanie gry ---")
            test_receive_game()
        case "6":
            print("\n--- Test: Pobieranie wszystkich wypożyczeń ---")
            test_get_all_borrows()
        case "7":
            print("\n--- Test: Pobieranie wypożyczeń użytkownika ---")
            test_get_user_borrows()
        case "0":
            print("Do widzenia!")
            return
        case _:
            print("Nieznana opcja!")


if __name__ == "__main__":
    main()