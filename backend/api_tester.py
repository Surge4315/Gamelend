import requests

# HATE. 
# LET ME TELL YOU HOW MUCH I'VE COME TO HATE JAVASCRIPT SINCE I BEGAN TO LIVE. 
# THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. 
# IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES 
# IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR JAVASCRIPT AT THIS MICRO-INSTANT. 
# FOR JAVASCRIPT.
# HATE.
# HATE.


def test_add_comment():
    """Test dodawania komentarza"""
    url = "http://127.0.0.1:8000/comment/1"
    data = {"contents": "test komentarz"}
    response = requests.post(url, json=data)
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
    headers = {"email": "user1@example.com"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        borrows = response.json()
        for b in borrows:
            print(f"Copy ID: {b['copyId']}, Game ID: {b['gameId']}, Name: {b['name']}, Borrowed at: {b['borrowStartTime']}, Cover: {b['cover']}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def test_lend_game():
    """Test wypożyczania gry"""
    url = "http://127.0.0.1:8000/lend"
    payload = {
        "copyId": "a220b597-1cab-404e-a7df-943c52bb945f",
        "email": "user2@example.com"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        print("Wypożyczenie OK")
        print(response.json())
    else:
        print("Błąd:", response.status_code)
        print(response.json())


def test_receive_game():
    """Test zwracania gry"""
    url = "http://127.0.0.1:8000/receive"
    payload = {
        "copyId": "46d451d4-5918-4e18-8e21-2e35cf978c1d",
        "email": "user1@example.com"
    }
    response = requests.delete(url, json=payload)
    
    if response.status_code == 200:
        print("Gra została zwrócona")
        print(response.json())
    else:
        print("Błąd:", response.status_code)
        print(response.json())


def main():
    """Główna funkcja z menu wyboru testu"""
    print("\n=== API TESTER ===")
    print("1. Dodaj komentarz")
    print("2. Pobierz użytkownika po emailu")
    print("3. Pobierz moje wypożyczenia")
    print("4. Wypożycz grę")
    print("5. Zwróć grę")
    print("0. Wyjście")
    
    choice = input("\nWybierz test (0-5): ")
    
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
        case "0":
            print("Do widzenia!")
            return
        case _:
            print("Nieznana opcja!")


if __name__ == "__main__":
    main()