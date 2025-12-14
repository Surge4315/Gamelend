-- Enable helpful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email                       CITEXT UNIQUE NOT NULL,
    password                    TEXT NOT NULL,
    provider                    TEXT NOT NULL DEFAULT 'local',
    is_verified                  BOOLEAN NOT NULL DEFAULT false,
    verification_token           TEXT,
    verification_token_expires    TIMESTAMPTZ,
    pending_email                CITEXT,
    email_change_token            TEXT,
    email_change_token_expires     TIMESTAMPTZ,
    password_reset_token          TEXT,
    password_reset_token_expires   TIMESTAMPTZ,
    is_deletion_pending           BOOLEAN NOT NULL DEFAULT false,
    deletion_scheduled_at         TIMESTAMPTZ
);

-- User roles
CREATE TABLE IF NOT EXISTS user_role (
    role        TEXT NOT NULL,
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (role, user_id)
);

CREATE INDEX IF NOT EXISTS idx_user_role_user_id ON user_role(user_id);

-- Refresh tokens
CREATE TABLE IF NOT EXISTS refresh_token (
    token       TEXT PRIMARY KEY,
    user_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_refresh_token_user_id ON refresh_token(user_id);
