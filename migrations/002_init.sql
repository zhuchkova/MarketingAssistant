CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    niche TEXT,
    offer TEXT,
    target_audience TEXT,
    expertise TEXT,
    tone TEXT,
    goal TEXT
);

CREATE TABLE audience_analyses (
    id UUID PRIMARY KEY,
    user_profile_id UUID UNIQUE NOT NULL
        REFERENCES user_profiles(id) ON DELETE CASCADE,
    audience_profile TEXT,
    pains TEXT,
    desires TEXT,
    objections TEXT,
    content_angles TEXT,
    tone TEXT,
    positioning TEXT,
    known_for TEXT
);

CREATE TABLE content_ideas (
    id UUID PRIMARY KEY,
    user_profile_id UUID NOT NULL
        REFERENCES user_profiles(id) ON DELETE CASCADE,
    audience_analysis_id UUID NOT NULL
        REFERENCES audience_analyses(id) ON DELETE CASCADE,
    title TEXT,
    hook TEXT,
    angle TEXT,
    topic TEXT
);

CREATE TABLE platforms (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE post_formats (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE post_goals (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE posts (
    id UUID PRIMARY KEY,
    user_profile_id UUID NOT NULL
        REFERENCES user_profiles(id) ON DELETE CASCADE,
    content_idea_id UUID
        REFERENCES content_ideas(id) ON DELETE SET NULL,
    platform_id INT NOT NULL
        REFERENCES platforms(id),
    post_format_id INT
        REFERENCES post_formats(id),
    post_goal_id INT
        REFERENCES post_goals(id),
    hook TEXT,
    body TEXT,
    cta TEXT,
    final_text TEXT
);

CREATE TABLE manychat_flows (
    id UUID PRIMARY KEY,
    post_id UUID UNIQUE NOT NULL
        REFERENCES posts(id) ON DELETE CASCADE,
    trigger_keyword TEXT,
    first_message TEXT,
    follow_up TEXT
);