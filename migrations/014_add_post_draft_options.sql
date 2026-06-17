ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS instagram_content_type TEXT,
    ADD COLUMN IF NOT EXISTS post_length TEXT DEFAULT 'medium';

UPDATE posts
SET post_length = 'medium'
WHERE post_length IS NULL;
