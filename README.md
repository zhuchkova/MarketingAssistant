# Marketing Assistant
This is my main Masterschool project.

User creates profile
    (it is saved in user_profiles table)
→ Audience Agent runs to analyze audience
    (saved in audience_analyses)
→ Idea Agent creates ideas
    (they are saved in content_ideas)

User selects idea, platform, format, goal
→ Content Agent creates one post
    (Post is saved in posts table)


RAG:
Audience Agent
    ↓
positioning_knowledge

Idea Agent
    ↓
idea_knowledge

Content Agent
    ↓
content_frameworks