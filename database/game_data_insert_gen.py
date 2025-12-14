import uuid
import random

NUM_GAMES = 500  # liczba gier do wygenerowania
COPIES_PER_GAME_MIN = 5
COPIES_PER_GAME_MAX = 50

# Możliwe wartości
categories = ['Action', 'Puzzle', 'Adventure', 'Strategy', 'RPG', 'FPS', 'Sports', 'Racing']
platforms = ['PS4', 'PS5', 'Xbox One', 'Xbox SX', 'Switch', 'Switch 2']
languages = ['PL', 'EN', 'DE', 'FR', 'ES', 'IT', 'JP']

# Przykładowe nazwy gier
game_name_prefixes = ['Dark', 'Final', 'Grand', 'Super', 'Legend', 'Ultimate', 'Cyber', 'Shadow', 'Mystic', 'Epic', 
                      'Ancient', 'Eternal', 'Royal', 'Dragon', 'Phoenix', 'Thunder', 'Crystal', 'Neon', 'Quantum', 'Stellar']
game_name_suffixes = ['Quest', 'Wars', 'Legends', 'Adventure', 'Chronicles', 'Battle', 'Arena', 'Journey', 'Saga', 'Heroes',
                      'Realm', 'Empire', 'Odyssey', 'Force', 'Strike', 'Tactics', 'Rivals', 'Destiny', 'Legacy', 'Warfare']

# Przykładowe studia
studios = ['GameStudio Inc', 'Epic Games', 'Pixel Forge', 'Neon Labs', 'Digital Dreams', 
           'Thunder Games', 'Infinity Studios', 'Blaze Interactive', 'Apex Gaming', 'Velocity Games']

def generate_game_name():
    return f'{random.choice(game_name_prefixes)} {random.choice(game_name_suffixes)} {random.randint(1, 10)}'

def generate_description():
    descriptions = [
        'An epic adventure awaits in this thrilling game.',
        'Experience the ultimate gaming experience with stunning graphics.',
        'Fight your way through challenging levels and bosses.',
        'Solve puzzles and uncover mysteries in this immersive world.',
        'Team up with friends in this multiplayer masterpiece.',
        'Explore vast open worlds filled with secrets and dangers.',
        'Master your skills and become the ultimate champion.',
        'A story-driven experience that will keep you on the edge of your seat.'
    ]
    return random.choice(descriptions)

games_inserts = []
categories_inserts = []
copies_inserts = []

# Zbiór unikalnych nazw gier
used_game_names = set()

# Generowanie gier
i = 1
while i <= NUM_GAMES:
    name = generate_game_name()
    
    # Sprawdzenie czy nazwa jest unikalna
    if name in used_game_names:
        continue  # Pomiń i generuj ponownie
    
    used_game_names.add(name)
    
    studio = random.choice(studios)
    description = generate_description()
    image_link = f'https://example.com/images/game{i}.jpg'
    
    # Liczba kopii dla tej gry
    num_copies = random.randint(COPIES_PER_GAME_MIN, COPIES_PER_GAME_MAX)
    
    # Escape single quotes w nazwach
    escaped_name = name.replace("'", "''")
    escaped_description = description.replace("'", "''")
    
    games_inserts.append(
        f'INSERT INTO game (name, image_link, description, studio, available_copies) '
        f"VALUES ('{escaped_name}', '{image_link}', '{escaped_description}', '{studio}', {num_copies});"
    )
    
    # Losowanie kategorii (1-3 kategorie na grę)
    num_categories = random.randint(1, 3)
    game_categories = random.sample(categories, num_categories)
    
    for cat in game_categories: 
        categories_inserts.append(
            f'INSERT INTO game_category (category, game_id) '
            f"VALUES ('{cat}', {i});"
        )
    
    # Generowanie kopii dla tej gry
    for _ in range(num_copies):
        lang = random.choice(languages)
        platform = random.choice(platforms)
        copies_inserts.append(
            f'INSERT INTO copy (game_id, lang_version, platform) '
            f"VALUES ({i}, '{lang}', '{platform}');"
        )
    
    i += 1

# Zapis do pliku .sql
with open('insert_games_data.sql', 'w', encoding='utf-8') as f:
    f.write('-- Inserting games\n')
    for line in games_inserts:
        f.write(line + '\n')
    
    f.write('\n-- Inserting game categories\n')
    for line in categories_inserts:
        f. write(line + '\n')
    
    f.write('\n-- Inserting game copies\n')
    for line in copies_inserts:
        f.write(line + '\n')

print(f"Plik insert_games_data.sql został wygenerowany.")
print(f"Wygenerowano {NUM_GAMES} unikalnych gier z łącznie {len(copies_inserts)} kopiami.")