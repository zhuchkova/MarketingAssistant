INSERT INTO users (id, name, email) VALUES
('11111111-1111-1111-1111-111111111111', 'Ekaterina', 'katya@example.com');

INSERT INTO user_profiles (
    id, user_id, niche, offer, target_audience, expertise, tone, goal
) VALUES (
    '22222222-2222-2222-2222-222222222222',
    '11111111-1111-1111-1111-111111111111',
    'AI automation for founders',
    'AI marketing workflows and systems',
    'early-stage founders struggling with marketing',
    'ML engineer building AI agents and automation systems',
    'bold, practical, slightly provocative',
    'generate leads and grow LinkedIn audience'
);

INSERT INTO audience_analyses (
    id,
    user_profile_id,
    audience_profile,
    pains,
    desires,
    objections,
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
    'replace marketing tasks with AI; simple workflows instead of tools; common founder mistakes; behind the scenes of building systems',
    'bold, direct, practical with actionable insights',
    'I help founders replace marketing tasks with AI workflows',
    'AI systems instead of marketing teams'
);

INSERT INTO content_ideas (
    id,
    user_profile_id,
    audience_analysis_id,
    title,
    hook,
    angle,
    topic
) VALUES
-- Idea 1
(
    '44444444-4444-4444-4444-444444444441',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    'You don’t need a marketing team',
    'Most founders don’t need a marketing team.',
    'contrarian',
    'AI marketing'
),

-- Idea 2
(
    '44444444-4444-4444-4444-444444444442',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    'Why your content does not convert',
    'Your content is not converting for one simple reason.',
    'pain_point',
    'content strategy'
),

-- Idea 3
(
    '44444444-4444-4444-4444-444444444443',
    '22222222-2222-2222-2222-222222222222',
    '33333333-3333-3333-3333-333333333333',
    '3 AI workflows for founders',
    '3 AI workflows every founder should use in 2026.',
    'how_to',
    'AI workflows'
);

INSERT INTO platforms (id, name) VALUES
(1, 'instagram'),
(2, 'linkedin');

INSERT INTO post_formats (id, name) VALUES
(1, 'story'),
(2, 'how_to'),
(3, 'list'),
(4, 'contrarian');

INSERT INTO post_goals (id, name) VALUES
(1, 'comment'),
(2, 'dm_keyword'),
(3, 'follow'),
(4, 'download');