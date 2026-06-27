ALTER TABLE automation_resources
    ADD COLUMN IF NOT EXISTS trigger_type TEXT DEFAULT 'specific_word',
    ADD COLUMN IF NOT EXISTS opening_dm_button_label TEXT,
    ADD COLUMN IF NOT EXISTS link_button_label TEXT,
    ADD COLUMN IF NOT EXISTS qualification_question TEXT,
    ADD COLUMN IF NOT EXISTS manychat_setup JSONB DEFAULT '{}'::jsonb;
