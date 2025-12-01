CREATE TABLE IF NOT EXISTS "RefreshToken" (
    token       TEXT PRIMARY KEY,
    userId      UUID NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_refreshToken_userId ON "RefreshToken"(userId);
