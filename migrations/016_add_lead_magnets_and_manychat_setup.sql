CREATE TABLE IF NOT EXISTS automation_resources (
    id UUID PRIMARY KEY,
    user_profile_id UUID NOT NULL
        REFERENCES user_profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    url TEXT,
    description TEXT,
    suggested_keyword TEXT,
    trigger_type TEXT DEFAULT 'specific_word',
    public_comment_reply TEXT,
    delivery_message TEXT,
    second_dm_message TEXT,
    opening_dm_button_label TEXT,
    link_button_label TEXT,
    qualification_question TEXT,
    follow_up_cta TEXT,
    preferred_post_goal TEXT,
    manychat_setup JSONB DEFAULT '{}'::jsonb,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE automation_resources
    ADD COLUMN IF NOT EXISTS public_comment_reply TEXT,
    ADD COLUMN IF NOT EXISTS second_dm_message TEXT,
    ADD COLUMN IF NOT EXISTS preferred_post_goal TEXT,
    ADD COLUMN IF NOT EXISTS trigger_type TEXT DEFAULT 'specific_word',
    ADD COLUMN IF NOT EXISTS opening_dm_button_label TEXT,
    ADD COLUMN IF NOT EXISTS link_button_label TEXT,
    ADD COLUMN IF NOT EXISTS qualification_question TEXT,
    ADD COLUMN IF NOT EXISTS manychat_setup JSONB DEFAULT '{}'::jsonb;

ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS automation_resource_id UUID
        REFERENCES automation_resources(id) ON DELETE SET NULL;

DROP TABLE IF EXISTS manychat_flows;
