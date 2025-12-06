CREATE TABLE IF NOT EXISTS "Game" (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT NOT NULL,
	image_link		TEXT NULL,	
    averageRate     NUMERIC(3,2) DEFAULT 0,
    nrOfRates       INT NOT NULL DEFAULT 0,
    studio          TEXT NOT NULL,
    availableCopies INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- if necessary: ALTER TYPE game_category ADD VALUE 'RPG';
CREATE TYPE game_category AS ENUM (
    'Action',
    'Puzzle',
    'Adventure',
    'Strategy',
	'RPG',
	'FPS',
	'Sports',
	'Racing'
);

CREATE TABLE IF NOT EXISTS "GameCategory" (
    category    game_category NOT NULL,
    gameId      UUID NOT NULL REFERENCES "Game"(id) ON DELETE CASCADE,
    PRIMARY KEY (category, gameId)
);

CREATE INDEX IF NOT EXISTS idx_gamecategory_gameId
    ON "GameCategory"(gameId);
	
	
CREATE TABLE IF NOT EXISTS "Comment" (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gameId      UUID NOT NULL REFERENCES "Game"(id) ON DELETE CASCADE,
    contents    TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comment_gameId ON "Comment"(gameId);

CREATE TYPE platform_type AS ENUM (
    'PS4',
    'PS5',
    'Xbox One',
	'Xbox SX',
    'Switch',
	'Switch 2'
);

CREATE TABLE IF NOT EXISTS "Copy" (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gameId      UUID NOT NULL REFERENCES "Game"(id) ON DELETE CASCADE,
    langVersion TEXT NOT NULL,
    platform    platform_type NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_copy_gameId ON "Copy"(gameId);

