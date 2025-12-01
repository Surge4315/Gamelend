CREATE TABLE IF NOT EXISTS "Borrow" (
    userId          UUID NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    copyId          UUID NOT NULL REFERENCES "Copy"(id) ON DELETE CASCADE,
    borrowStartTime TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (userId, copyId)
);

CREATE INDEX IF NOT EXISTS idx_borrow_copyId ON "Borrow"(copyId);
