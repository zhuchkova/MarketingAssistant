ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS published_url TEXT;

UPDATE posts
SET created_at = COALESCE(created_at, published_at, NOW())
WHERE created_at IS NULL;
