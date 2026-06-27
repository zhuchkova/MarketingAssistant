ALTER TABLE automation_resources
    ADD COLUMN IF NOT EXISTS public_comment_reply TEXT,
    ADD COLUMN IF NOT EXISTS preferred_post_goal TEXT,
    ADD COLUMN IF NOT EXISTS trigger_type TEXT DEFAULT 'specific_word',
    ADD COLUMN IF NOT EXISTS opening_dm_button_label TEXT,
    ADD COLUMN IF NOT EXISTS link_button_label TEXT,
    ADD COLUMN IF NOT EXISTS qualification_question TEXT,
    ADD COLUMN IF NOT EXISTS manychat_setup JSONB DEFAULT '{}'::jsonb;

ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS automation_resource_id UUID
        REFERENCES automation_resources(id) ON DELETE SET NULL;
