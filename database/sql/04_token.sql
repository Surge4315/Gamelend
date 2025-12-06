CREATE TABLE IF NOT EXISTS "RefreshToken" (
    token       TEXT PRIMARY KEY,
    userId      UUID NOT NULL REFERENCES "User"(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_refreshToken_userId ON "RefreshToken"(userId);
