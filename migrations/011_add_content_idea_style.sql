ALTER TABLE content_ideas
    ADD COLUMN IF NOT EXISTS content_style TEXT;

UPDATE content_ideas
SET content_style = CASE
    WHEN angle IN ('story', 'personal_story') THEN 'personal_story'
    WHEN angle IN ('how_to', 'how-to') THEN 'how_to'
    WHEN angle IN ('list', 'checklist') THEN 'checklist'
    WHEN angle = 'pain_point' THEN 'objection_handling'
    WHEN angle = 'contrarian' THEN 'contrarian'
    ELSE COALESCE(NULLIF(angle, ''), 'quick_tip')
END
WHERE content_style IS NULL;

SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);

INSERT INTO post_formats (name) VALUES
    ('personal_story'),
    ('mistakes'),
    ('day_in_life'),
    ('contrarian'),
    ('how_to'),
    ('checklist'),
    ('myth_busting'),
    ('before_after'),
    ('opinion'),
    ('client_example'),
    ('behind_scenes'),
    ('faq'),
    ('comparison'),
    ('quick_tip'),
    ('lessons_learned'),
    ('case_study'),
    ('trend_take'),
    ('resource_list'),
    ('framework'),
    ('objection_handling')
ON CONFLICT (name) DO NOTHING;

SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);
