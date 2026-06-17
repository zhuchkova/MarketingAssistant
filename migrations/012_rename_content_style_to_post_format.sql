ALTER TABLE content_ideas
    ADD COLUMN IF NOT EXISTS post_format TEXT;

UPDATE content_ideas
SET post_format = COALESCE(post_format, content_style, angle, 'how_to')
WHERE post_format IS NULL;

UPDATE content_ideas
SET post_format = CASE
    WHEN post_format IN ('story', 'personal_story') THEN 'personal_story'
    WHEN post_format IN ('mistake', 'mistakes') THEN 'mistakes'
    WHEN post_format IN ('day_in_life', 'a_day_in_the_life') THEN 'day_in_life'
    WHEN post_format IN ('how_to', 'how-to', 'tutorial') THEN 'how_to'
    WHEN post_format IN ('list', 'checklist') THEN 'checklist'
    WHEN post_format IN ('myth_busting', 'myth') THEN 'myth_busting'
    WHEN post_format IN ('case_study', 'client_example') THEN 'client_example'
    WHEN post_format IN ('behind_scenes', 'behind_the_scenes') THEN 'behind_scenes'
    WHEN post_format IN ('objection_handling', 'pain_point') THEN 'objection_handling'
    WHEN post_format = 'contrarian' THEN 'contrarian'
    ELSE 'how_to'
END;

SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);

INSERT INTO post_formats (name) VALUES
    ('personal_story'),
    ('mistakes'),
    ('day_in_life'),
    ('contrarian'),
    ('how_to'),
    ('checklist'),
    ('myth_busting'),
    ('client_example'),
    ('behind_scenes'),
    ('objection_handling')
ON CONFLICT (name) DO NOTHING;

DELETE FROM post_formats pf
WHERE pf.name IN (
    'story',
    'list',
    'before_after',
    'opinion',
    'faq',
    'comparison',
    'quick_tip',
    'lessons_learned',
    'case_study',
    'trend_take',
    'resource_list',
    'framework'
)
AND NOT EXISTS (
    SELECT 1
    FROM posts p
    WHERE p.post_format_id = pf.id
);

SELECT setval(pg_get_serial_sequence('post_formats', 'id'), COALESCE((SELECT MAX(id) FROM post_formats), 1), true);
