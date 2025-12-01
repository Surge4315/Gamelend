CREATE TABLE IF NOT EXISTS "User" (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email                       CITEXT UNIQUE NOT NULL,
    password                    TEXT NOT NULL,
    provider                    TEXT NOT NULL DEFAULT 'local',
    isVerified                  BOOLEAN NOT NULL DEFAULT false,
    verificationToken           TEXT,
    verificationTokenExpires    TIMESTAMPTZ,
    pendingEmail                CITEXT,
    emailChangeToken            TEXT,
    emailChangeTokenExpires     TIMESTAMPTZ,
    passwordResetToken          TEXT,
    passwordResetTokenExpires   TIMESTAMPTZ,
    isDeletionPending           BOOLEAN NOT NULL DEFAULT false,
    deletionScheduledAt         TIMESTAMPTZ,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "UserRole" (
    role        TEXT NOT NULL,
    userId      UUID NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
    PRIMARY KEY (role, userId)
);

CREATE INDEX IF NOT EXISTS idx_userrole_userId ON "UserRole"(userId);