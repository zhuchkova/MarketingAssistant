ALTER TABLE user_profiles
    ADD COLUMN IF NOT EXISTS personal_touch TEXT,
    ADD COLUMN IF NOT EXISTS market_scope TEXT,
    ADD COLUMN IF NOT EXISTS primary_market TEXT,
    ADD COLUMN IF NOT EXISTS currency TEXT,
    ADD COLUMN IF NOT EXISTS locale_notes TEXT;

ALTER TABLE audience_analyses
    ADD COLUMN IF NOT EXISTS trigger_moments JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS proof_points JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS audience_language JSONB DEFAULT '[]'::jsonb,
    ADD COLUMN IF NOT EXISTS market_context JSONB DEFAULT '[]'::jsonb;

ALTER TABLE content_ideas
    ADD COLUMN IF NOT EXISTS post_format TEXT,
    ADD COLUMN IF NOT EXISTS content_style TEXT;

INSERT INTO users (id, name, email) VALUES
('11111111-1111-1111-1111-111111111111', 'Ekaterina', 'katya@example.com')
ON CONFLICT (id) DO NOTHING;

INSERT INTO user_profiles (
    id, user_id, niche, offer, target_audience, expertise, personal_touch,
    market_scope, primary_market, currency, locale_notes, tone, goal
) VALUES (
    '22222222-2222-2222-2222-222222222222',
    '11111111-1111-1111-1111-111111111111',
    'AI automation for founders',
    'AI marketing workflows and systems',
    'early-stage founders struggling with marketing',
    'ML engineer building AI agents and automation systems',
    'I started by building these workflows manually for my own projects before turning them into repeatable AI systems.',
    'global',
    'Online English-speaking founders',
    'USD',
    'Write in English and avoid overly local references unless provided.',
    'bold, practical, slightly provocative',
    'generate leads and grow LinkedIn audience'
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO audience_analyses (
    id,
    user_profile_id,
    audience_profile,
    pains,
    desires,
    objections,
    trigger_moments,
    proof_points,
    audience_language,
    market_context,
    content_angles,
    tone,
    positioning,
    known_for
) VALUES (
    '33333333-3333-3333-3333-333333333333',
    '22222222-2222-2222-2222-222222222222',
    'Early-stage founders who lack time and resources to build consistent marketing systems',
    'no time for marketing; inconsistent posting; low engagement; confusion about what works',
    'predictable lead generation; simple systems; authority in their niche',
    'AI feels too complex; content feels fake; no time to learn new tools',
    '["after a quiet launch", "when content takes too long", "when founders need leads but cannot hire a marketing team"]',
    '["before-after workflow examples", "time saved by automation", "simple founder-specific systems"]',
    '["I do not have time for marketing", "AI content sounds fake", "I need leads but cannot hire a team"]',
    '["Global online market", "Use USD only when prices are mentioned", "Write in English for founders across regions"]',
    'replace marketing tasks with AI; simple workflows instead of tools; common founder mistakes; behind the scenes of building systems',
    'bold, direct, practical with actionable insights',
    'I help founders replace marketing tasks with AI workflows',
    'AI systems instead of marketing teams'
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO content_ideas (
    id,
    user_profile_id,
    audience_analysis_id,
    title,
    hook,
    angle,
    topic,
    post_format,
    content_style
) VALUES
-- Idea 1
(
    '44444444-4444-4444-4444-444444444441',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    'You don’t need a marketing team',
    'Most founders don’t need a marketing team.',
    'contrarian',
    'AI marketing',
    'contrarian',
    'contrarian'
),

-- Idea 2
(
    '44444444-4444-4444-4444-444444444442',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    'Why your content does not convert',
    'Your content is not converting for one simple reason.',
    'pain_point',
    'content strategy',
    'objection_handling',
    'objection_handling'
),

-- Idea 3
(
    '44444444-4444-4444-4444-444444444443',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    '3 AI workflows for founders',
    '3 AI workflows every founder should use in 2026.',
    'how_to',
    'AI workflows',
    'how_to',
    'how_to'
)
ON CONFLICT (id) DO NOTHING;

INSERT INTO platforms (id, name) VALUES
(1, 'instagram'),
(2, 'linkedin')
ON CONFLICT (id) DO NOTHING;

INSERT INTO post_formats (id, name) VALUES
(1, 'story'),
(2, 'how_to'),
(3, 'list'),
(4, 'contrarian')
ON CONFLICT (id) DO NOTHING;

SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);

INSERT INTO post_formats (name) VALUES
('personal_story'),
('mistakes'),
('day_in_life'),
('checklist'),
('myth_busting'),
('client_example'),
('behind_scenes'),
('objection_handling')
ON CONFLICT (name) DO NOTHING;

INSERT INTO post_goals (id, name) VALUES
(1, 'comment'),
(2, 'dm_keyword'),
(3, 'follow'),
(4, 'download')
ON CONFLICT (id) DO NOTHING;

SELECT setval(pg_get_serial_sequence('post_goals', 'id'), COALESCE((SELECT MAX(id) FROM post_goals), 1), true);

INSERT INTO post_goals (name) VALUES
('share'),
('save'),
('book_visit'),
('buy_order')
ON CONFLICT (name) DO NOTHING;

SELECT setval(pg_get_serial_sequence('platforms', 'id'), COALESCE((SELECT MAX(id) FROM platforms), 1), true);
SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);
SELECT setval(pg_get_serial_sequence('post_goals', 'id'), COALESCE((SELECT MAX(id) FROM post_goals), 1), true);
