INSERT INTO posts (
    id,
    user_profile_id,
    content_idea_id,
    platform_id,
    post_format_id,
    post_goal_id,
    hook,
    body,
    cta,
    final_text
) VALUES (
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222',
    '44444444-4444-4444-4444-444444444441',
    2, -- LinkedIn
    4, -- contrarian
    2, -- dm_keyword
    'Most founders don’t need a marketing team.',
    'They need 3 AI workflows that generate ideas, write posts, and convert leads automatically.',
    'Comment AGENT and I will send you the system.',
    'Most founders don’t need a marketing team.\n\nThey need 3 AI workflows that generate ideas, write posts, and convert leads automatically.\n\nComment AGENT and I will send you the system.'
)
ON CONFLICT (id) DO NOTHING;
