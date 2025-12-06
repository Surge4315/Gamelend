CREATE TABLE IF NOT EXISTS borrow (
    user_id          UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    copy_id          UUID NOT NULL REFERENCES copy(id) ON DELETE CASCADE,
    borrow_start_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, copy_id)
);

CREATE INDEX IF NOT EXISTS idx_borrow_copy_id ON borrow(copy_id);
