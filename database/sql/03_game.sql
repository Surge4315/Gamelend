CREATE TABLE IF NOT EXISTS game (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT NOT NULL,
	image_link		TEXT,	
	description		TEXT NOT NULL,
    studio          TEXT NOT NULL,
    available_copies INT NOT NULL DEFAULT 0
);

-- if necessary: ALTER TYPE game_category ADD VALUE 'RPG';
CREATE TYPE game_categories AS ENUM (
    'Action',
    'Puzzle',
    'Adventure',
    'Strategy',
	'RPG',
	'FPS',
	'Sports',
	'Racing'
);

CREATE TABLE IF NOT EXISTS game_category (
    category    game_categories NOT NULL,
    game_id      UUID NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    PRIMARY KEY (category, game_id)
);

CREATE INDEX IF NOT EXISTS idx_game_category_game_id
    ON game_category(game_id);
	
	
CREATE TABLE IF NOT EXISTS comment (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id      UUID NOT NULL REFERENCES game(id) ON DELETE CASCADE,
	user_id		UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    contents    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_comment_game_id ON comment(game_id);

CREATE TYPE platform_type AS ENUM (
    'PS4',
    'PS5',
    'Xbox One',
	'Xbox SX',
    'Switch',
	'Switch 2'
);

CREATE TABLE IF NOT EXISTS copy (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id      UUID NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    lang_version TEXT NOT NULL,
    platform    platform_type NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_copy_game_id ON copy(game_id);

