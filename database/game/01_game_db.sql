-- Enable helpful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Game table
CREATE TABLE IF NOT EXISTS game (
    id         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name            TEXT NOT NULL,
    image_link      TEXT,
    description     TEXT NOT NULL,
    studio          TEXT NOT NULL,
    available_copies INT NOT NULL DEFAULT 0
);

-- Game categories enum
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

-- Game category table
CREATE TABLE IF NOT EXISTS game_category (
    category    game_categories NOT NULL,
    game_id 	INT NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    PRIMARY KEY (category, game_id)
);

CREATE INDEX IF NOT EXISTS idx_game_category_game_id
    ON game_category(game_id);

-- Platform type enum
CREATE TYPE platform_type AS ENUM (
    'PS4',
    'PS5',
    'Xbox One',
    'Xbox SX',
    'Switch',
    'Switch 2'
);

-- Copy table
CREATE TABLE IF NOT EXISTS copy (
    copy_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    game_id      	 INT NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    lang_version TEXT NOT NULL,
    platform     platform_type NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_copy_game_id ON copy(game_id);

-- Comment table
CREATE TABLE IF NOT EXISTS comment (
    id 			INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    game_id     INT NOT NULL REFERENCES game(id) ON DELETE CASCADE,
    contents    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_comment_game_id ON comment(game_id);

-- Borrow table (user_id without FK)
CREATE TABLE IF NOT EXISTS borrow (
    user_id          UUID NOT NULL,
    copy_id          INT NOT NULL REFERENCES copy(copy_id) ON DELETE CASCADE,
    borrow_start_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, copy_id)
);

CREATE INDEX IF NOT EXISTS idx_borrow_copy_id ON borrow(copy_id);
