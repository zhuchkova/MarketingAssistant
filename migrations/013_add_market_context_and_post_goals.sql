ALTER TABLE user_profiles
    ADD COLUMN IF NOT EXISTS market_scope TEXT,
    ADD COLUMN IF NOT EXISTS primary_market TEXT,
    ADD COLUMN IF NOT EXISTS currency TEXT,
    ADD COLUMN IF NOT EXISTS locale_notes TEXT;

ALTER TABLE audience_analyses
    ADD COLUMN IF NOT EXISTS market_context JSONB DEFAULT '[]'::jsonb;

SELECT setval(pg_get_serial_sequence('post_goals', 'id'), COALESCE((SELECT MAX(id) FROM post_goals), 1), true);

INSERT INTO post_goals (name) VALUES
    ('share'),
    ('save'),
    ('book_visit'),
    ('buy_order')
ON CONFLICT (name) DO NOTHING;

SELECT setval(pg_get_serial_sequence('post_goals', 'id'), COALESCE((SELECT MAX(id) FROM post_goals), 1), true);
