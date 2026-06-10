-- Add password auth to existing users table
ALTER TABLE users
    ADD COLUMN IF NOT EXISTS hashed_password TEXT,
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW();

-- name was NOT NULL but we don't collect it on signup
ALTER TABLE users ALTER COLUMN name DROP NOT NULL;