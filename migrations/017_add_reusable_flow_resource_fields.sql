ALTER TABLE lead_magnets
    ADD COLUMN IF NOT EXISTS public_comment_reply TEXT,
    ADD COLUMN IF NOT EXISTS preferred_post_goal TEXT;

ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS lead_magnet_id UUID
        REFERENCES lead_magnets(id) ON DELETE SET NULL;
