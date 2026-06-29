ALTER TABLE content_ideas
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

UPDATE content_ideas
SET created_at = COALESCE(created_at, NOW())
WHERE created_at IS NULL;
