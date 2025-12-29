import requests

# HATE. 
# LET ME TELL YOU HOW MUCH I'VE COME TO HATE JAVASCRIPT SINCE I BEGAN TO LIVE. 
# THERE ARE 387.44 MILLION MILES OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. 
# IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE HUNDREDS OF MILLIONS OF MILES 
# IT WOULD NOT EQUAL ONE ONE-BILLIONTH OF THE HATE I FEEL FOR JAVASCRIPT AT THIS MICRO-INSTANT. 
# FOR JAVASCRIPT.
# HATE.
# HATE.
'''
url = "http://127.0.0.1:8000/comment/1"
data = {"contents": "test komentarz"}

response = requests.post(url, json=data)
print(response.json())
'''

'''
# Endpoint GET z parametrem email
url = "http://127.0.0.1:8001/by-email"
params = {"email": "user1@example.com"}  # tutaj podajesz email którego szukasz

response = requests.get(url, params=params)

# Wypisanie odpowiedzi JSON
print(response.json())
'''

# Endpoint GET z nagłówkiem email
url = "http://127.0.0.1:8000/my-borrows"  # tutaj Twój endpoint
headers = {"email": "user1@example.com"}  # podaj email użytkownika

response = requests.get(url, headers=headers)

if response.status_code == 200:
    borrows = response.json()
    for b in borrows:
        print(f"Copy ID: {b['copyId']}, Game ID: {b['gameId']}, Name: {b['name']}, Borrowed at: {b['borrowStartTime']}, Cover: {b['cover']}")
else:
    print(f"Error: {response.status_code}, {response.text}")