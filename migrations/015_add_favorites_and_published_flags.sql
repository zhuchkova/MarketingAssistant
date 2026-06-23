ALTER TABLE content_ideas
    ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE;

ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS is_published BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS published_at TIMESTAMP;

UPDATE content_ideas
SET is_favorite = FALSE
WHERE is_favorite IS NULL;

UPDATE posts
SET is_favorite = FALSE
WHERE is_favorite IS NULL;

UPDATE posts
SET is_published = FALSE
WHERE is_published IS NULL;
