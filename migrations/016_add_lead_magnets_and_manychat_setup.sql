CREATE TABLE IF NOT EXISTS lead_magnets (
    id UUID PRIMARY KEY,
    user_profile_id UUID NOT NULL
        REFERENCES user_profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    url TEXT,
    description TEXT,
    suggested_keyword TEXT,
    public_comment_reply TEXT,
    delivery_message TEXT,
    follow_up_cta TEXT,
    preferred_post_goal TEXT,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE lead_magnets
    ADD COLUMN IF NOT EXISTS public_comment_reply TEXT,
    ADD COLUMN IF NOT EXISTS preferred_post_goal TEXT;

ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS lead_magnet_id UUID
        REFERENCES lead_magnets(id) ON DELETE SET NULL;

ALTER TABLE manychat_flows
    ADD COLUMN IF NOT EXISTS lead_magnet_id UUID REFERENCES lead_magnets(id) ON DELETE SET NULL,
    ADD COLUMN IF NOT EXISTS public_comment_reply TEXT,
    ADD COLUMN IF NOT EXISTS manychat_setup JSONB DEFAULT '{}'::jsonb;
