import uuid
import random

NUM_USERS = 10_000  # liczba użytkowników do wygenerowania
PASSWORD = '$argon2id$v=19$m=65536,t=3,p=4$K8nkX7fnQZ0j6uRm1Y5+fg$fyP+UDBqdcwz4rHciaG98AIOudBabE3jwqyI73oiLSg'

def random_email(i):
    return f'user{i}@example.com'

# Prawdopodobieństwo provider
providers = ['local']*7 + ['google']*3
roles = ['USER']*999 + ['ADMIN']*1

users_inserts = []
roles_inserts = []

for i in range(1, NUM_USERS + 1):
    user_id = str(uuid.uuid4())
    email = random_email(i)
    provider = random.choice(providers)
    is_verified = 'true'
    
    users_inserts.append(
        f'INSERT INTO users (id, email, provider, password, is_verified) '
        f"VALUES ('{user_id}', '{email}', '{provider}', '{PASSWORD}', {is_verified});"
    )
    
    # Losowanie ról
    user_roles = set()
    role = random.choice(roles)
    user_roles.add(role)
    if role == 'ADMIN':
        user_roles.add('USER')  # ADMIN musi mieć też USER
    
    for r in user_roles:
        roles_inserts.append(
            f'INSERT INTO user_role (user_id, role) '
            f"VALUES ('{user_id}', '{r}');"
        )

# Zapis do pliku .sql
with open('insert_data.sql', 'w') as f:
    for line in users_inserts + roles_inserts:
        f.write(line + '\n')

print("Plik insert_data.sql został wygenerowany.")
