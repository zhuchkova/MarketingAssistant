# Marketing Assistant

AI-powered marketing automation platform that helps creators, coaches, founders, and experts generate audience-specific social media content.

Built as part of the **Masterschool AI Engineering Program**.

---

## Overview

Marketing Assistant is an AI-driven platform designed to automate key marketing activities that are typically handled by a marketing team.

The system combines **LLMs, RAG (Retrieval-Augmented Generation), LangChain, ChromaDB, FastAPI, and PostgreSQL** to:

* Analyze a creator's positioning and audience
* Generate content ideas and hooks
* Create platform-specific posts for LinkedIn and Instagram
* Generate Instagram conversion funnels and ManyChat-style automations

The goal is to provide highly relevant, engaging, and conversion-oriented content rather than generic AI-generated posts.

Each signed-in user can manage multiple marketing profiles (for example: LinkedIn Personal Brand, AI Consulting Business, Fitness Coaching Brand), each with its own audience analysis, content ideas, posts, and Instagram conversion funnels.

---

## Architecture

```text
User
  │
  ▼
Sign up / Sign in
  │
  ▼
Marketing Profile
  │
  ▼
Audience Agent
  │
  ▼
Audience Analysis
  │
  ▼
Idea Agent
  │
  ▼
Content Ideas
  │
  ▼
Content Agent
  │
  ▼
Generated Posts
  │
  ▼
Automation Agent
  │
  ▼
ManyChat Funnel
```

---

## AI Agents

### 1. Audience Agent

Analyzes a creator profile and generates:

* Audience profile
* Audience pains
* Audience desires
* Audience objections
* Content angles
* Recommended tone
* Positioning statement
* "Known for" statement

#### Input

* Profile Name
* Niche
* Offer
* Target Audience
* Expertise
* Personal Touch
* Market Scope
* Primary Market
* Currency
* Tone
* Goal

#### Output

* Audience Analysis

---

### 2. Idea Agent

Generates content ideas based on:

* Creator profile
* Audience analysis
* Marketing knowledge stored in ChromaDB

#### Output

* Title
* Hook
* Idea framing
* Topic
* Post format, such as personal story, mistakes, day in the life, contrarian, how-to, checklist, myth busting, or client example

#### Idea field definitions

* `post_format` is the structure of the post. It must match one of the approved `post_formats` lookup values.
* `angle` is stored as the idea framing: the specific point of view or strategic framing for the idea.
* `topic` is the subject the post is about.

---

### 3. Content Agent

Creates a post draft from a saved content idea.

Draft controls:

* `platform`: `instagram` or `linkedin`
* `instagram_content_type`: `carousel`, `story`, or `reel` when platform is Instagram
* `post_length`: `short`, `medium`, or `long`
* `post_goal`: comment, DM keyword, save, follow, download, share, book/visit, or buy/order
* optional `automation_resource_id`: a saved Instagram DM resource that the CTA should use

Generates complete LinkedIn or Instagram posts.

#### Input

* Content Idea
* Platform
* Format
* Goal
* Optional saved DM resource for Instagram CTA alignment

#### Output

* Hook
* Body
* CTA
* Final Post

---

### 4. Automation Agent

Creates reusable ManyChat-style Instagram comment-to-DM automations from DM resources.

#### Output

* Trigger Keyword
* First Message
* Qualification Question
* Follow-up Message

---

## RAG Architecture

The project uses **ChromaDB** as a vector database.

### positioning_knowledge

Used by the Audience Agent.

Contains:

* Positioning frameworks
* Audience analysis frameworks
* Expert positioning examples

---

### idea_knowledge

Used by the Idea Agent.

Contains:

* Hook patterns
* Viral content structures
* Content angle frameworks

---

### content_frameworks

Used by the Content Agent.

Contains:

* Storytelling frameworks
* Contrarian post structures
* Educational content structures
* CTA patterns

---

### cta_patterns

Used by the Automation Agent.

Contains:

* CTA best practices
* DM resource strategies
* Comment-to-DM patterns

---

### comment_automation_templates

Used by the Automation Agent.

Contains:

* Funnel templates
* Qualification flows
* Follow-up message examples

---

## Database

### PostgreSQL

Stores application data.

#### Core Tables

```text
users
  ├── email
  ├── name
  └── hashed_password

user_profiles
  ├── profile_name
  ├── niche
  ├── offer
  ├── target_audience
  ├── expertise
  ├── personal_touch
  ├── market_scope
  ├── primary_market
  ├── currency
  ├── locale_notes
  ├── tone
  └── goal

audience_analyses
  ├── audience_profile
  ├── pains
  ├── desires
  ├── objections
  ├── trigger_moments
  ├── proof_points
  ├── audience_language
  ├── market_context
  ├── content_angles
  ├── tone
  ├── positioning
  └── known_for
content_ideas
  ├── title
  ├── hook
  ├── angle
  ├── topic
  ├── trend_context
  ├── post_format
  ├── created_at
  └── is_favorite
posts
  ├── automation_resource_id
  ├── instagram_content_type
  ├── post_length
  ├── created_at
  ├── is_favorite
  ├── is_published
  ├── published_at
  ├── published_url
  ├── hook
  ├── body
  ├── cta
  └── final_text
automation_resources
  ├── title
  ├── url
  ├── description
  ├── suggested_keyword
  ├── trigger_type
  ├── public_comment_reply
  ├── delivery_message
  ├── second_dm_message
  ├── opening_dm_button_label
  ├── link_button_label
  ├── qualification_question
  ├── follow_up_cta
  ├── preferred_post_goal
  ├── manychat_setup
  └── is_primary
```

### ChromaDB

Stores marketing knowledge used by RAG agents.

---

## Local Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/marketing_assistant
JWT_SECRET_KEY=replace-with-a-long-random-secret
OPENAI_API_KEY=sk-...
FRONTEND_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
AUDIENCE_AGENT_MODEL=openai:gpt-4o-mini
IDEA_AGENT_MODEL=openai:gpt-4o-mini
CONTENT_AGENT_MODEL=openai:gpt-4o-mini
AUTOMATION_AGENT_MODEL=openai:gpt-4o-mini
```

`DATABASE_URL` is required by FastAPI endpoints and `scripts/migrate.py`.

`JWT_SECRET_KEY` signs login tokens and is required. The API will reject token operations if this is missing.

`OPENAI_API_KEY` is required by the LangChain/OpenAI agents. Agent model defaults are configured in `agents/model_config.py` and can be overridden in `.env`:

| Variable | Default | Used for |
| --- | --- | --- |
| `AUDIENCE_AGENT_MODEL` | `openai:gpt-4o-mini` | Audience analysis |
| `IDEA_AGENT_MODEL` | `openai:gpt-4o-mini` | Content idea generation |
| `CONTENT_AGENT_MODEL` | `openai:gpt-4o-mini` | Post drafting and revisions |
| `AUTOMATION_AGENT_MODEL` | `openai:gpt-4o-mini` | Instagram comment-to-DM automation flows |

Use only model IDs your OpenAI project can access. If a model returns `403 model_not_found`, set that agent back to a model available to your API key, such as `openai:gpt-4o-mini`.

`FRONTEND_ORIGINS` is a comma-separated CORS allowlist. For production, set it to your deployed frontend URL.

### 4. Run database migrations

```bash
python scripts/migrate.py
```

This creates and updates the PostgreSQL schema, including user auth fields.

### 5. Seed ChromaDB knowledge

RAG seed data lives in `rag_seed_data/` as editable JSON knowledge cards. To rebuild local RAG data, run the combined seed script from the project root:

```bash
python scripts/seed_chroma_all.py
```

The seed script uses `upsert`, so rerunning it updates existing cards with the same IDs. Add new cards to the matching file:

* `positioning_knowledge/` for audience research, positioning, pains, desires, objections, and voice-of-customer patterns. This collection is split into smaller JSON files so editors can open them comfortably.
* `idea_knowledge.json` for hook patterns, content angles, belief shifts, and audience-specific idea triggers.
* `content_frameworks.json` for LinkedIn structures, Instagram carousel/story/Reel structures, and length rules.
* `cta_patterns.json` for comment, DM, save, follow, download, share, book/visit, buy/order, public reply, and no-guide fallback CTA patterns.
* `comment_automation_templates.json` for keyword flows, public comment replies, first messages, qualifying questions, follow-ups, DM resource delivery, no-guide fallbacks, and manual ManyChat setup JSON.

To inspect the current Chroma collections:

```bash
python scripts/debug_chroma.py
```

`scripts/reset_chroma.py` currently deletes only the `positioning_knowledge` collection. If you want a full reset, delete `chroma_db` locally and rerun `python scripts/seed_chroma_all.py`.

### 6. Start the app

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

### 7. Run tests

```bash
python -m unittest discover -s tests
```

---

## API Endpoints

Most application endpoints require a JWT bearer token returned by `/auth/register` or `/auth/login`.

```http
Authorization: Bearer <token>
```

### Authentication

#### Register

```http
POST /auth/register
```

Creates a user, stores a bcrypt password hash, and returns a JWT token.

Passwords must be at least 8 characters.

```json
{
  "email": "creator@example.com",
  "password": "secure-password",
  "name": "Creator Name"
}
```

#### Login

```http
POST /auth/login
```

Validates the email and password, then returns a JWT token.

```json
{
  "email": "creator@example.com",
  "password": "secure-password"
}
```

#### Sign Out

There is no server-side logout endpoint because authentication uses stateless JWTs. The frontend signs the user out by deleting the saved token from browser storage and returning to the auth screen.

Tokens expire after 7 days. To invalidate tokens immediately across devices, add server-side token revocation or shorter token lifetimes.

---

### Users

#### Get My Profiles

```http
GET /users/me/profiles
```

Returns all marketing profiles belonging to the signed-in user.

---

### Profiles

#### Create Profile

```http
POST /user-profiles
```

Creates a marketing profile for the signed-in user. The client no longer sends `user_id`; the backend reads it from the JWT.
The backend can generate the profile ID automatically if the request does not include one.

Triggers:

```text
Audience Agent
↓
Idea Agent
```

#### Update Profile

```http
PUT /user-profiles/{profile_id}
```

Regenerates:

```text
Audience Analysis
↓
Content Ideas
```

Existing posts are preserved. Favorite ideas are preserved; non-favorite ideas are replaced with fresh ideas.

#### Get Profile

```http
GET /user-profiles/{profile_id}
```

#### Get Audience Analysis

```http
GET /user-profiles/{profile_id}/audience-analysis
```

#### Get Content Ideas

```http
GET /user-profiles/{profile_id}/content-ideas
```

#### Favorite Idea

```http
PUT /content-ideas/{idea_id}/favorite
```

Toggles whether an idea is saved as a favorite. Favorite ideas are preserved when ideas are regenerated.

---

### Posts

#### Generate Post

```http
POST /posts
```

Triggers:

```text
Content Agent
```

#### Get Post

```http
GET /posts/{post_id}
```

#### Get All Posts for a Profile

```http
GET /user-profiles/{profile_id}/posts
```

#### Favorite Post

```http
PUT /posts/{post_id}/favorite
```

Toggles whether a post is saved as a favorite.

#### Published Post

```http
PUT /posts/{post_id}/published
```

Toggles whether a post is marked as published. The frontend marks a post as published automatically when the full post text is copied.

#### Delete Post

```http
DELETE /posts/{post_id}
```

---

### Automations

Automation setup is optional and happens after the main profile workflow. A user can create a profile, review audience analysis, generate ideas, and draft posts without adding any DM resource or ManyChat setup.

In the frontend, reusable DM resources are managed from the **Automations** dashboard tab. The intended workflow is:

1. Add one or more resources, such as a guide, booking page, product page, class details, or a conversation offer.
2. Generate one automation or regenerate all automations. The app prepares the keyword mode, keyword, public reply, opening DM, button labels, optional qualification question, follow-up, and ManyChat setup JSON.
3. Draft Instagram reels/carousels and optionally select one prepared automation so the Content Agent writes the CTA around the real keyword and promise.

LinkedIn posts and Instagram Stories do not use comment-to-DM automation selectors.

#### Profile DM Resources

```http
GET /user-profiles/{profile_id}/automation-resources
POST /user-profiles/{profile_id}/automation-resources
POST /user-profiles/{profile_id}/automation-resources/{automation_resource_id}/generate-automation
POST /user-profiles/{profile_id}/automation-resources/regenerate-automations
PUT /user-profiles/{profile_id}/automation-resources/{automation_resource_id}
DELETE /user-profiles/{profile_id}/automation-resources/{automation_resource_id}
```

DM resources are optional reusable resources for Instagram comment-to-DM automations. The URL is optional so an automation can send a link, booking details, order instructions, or simply start a conversation. A generated automation can store trigger mode, keyword, public reply, first DM, opening button label, link button label, optional qualification question, optional follow-up, preferred post goal, and setup JSON.

#### Get Post Automation Setup

```http
GET /posts/{post_id}/automation
```

This endpoint only previews the reusable automation already attached to the Instagram reel/carousel post through `posts.automation_resource_id`. It does not generate or store a post-specific ManyChat flow.

---

## Example Requests

Examples below assume the app is running at `http://127.0.0.1:8000`.

### Register Request

```json
{
  "email": "creator@example.com",
  "password": "secure-password",
  "name": "Creator Name"
}
```

### Register Response

```json
{
  "token": "JWT_TOKEN",
  "user_id": "11111111-1111-1111-1111-111111111111",
  "email": "creator@example.com",
  "name": "Creator Name"
}
```

### Login Request

```json
{
  "email": "creator@example.com",
  "password": "secure-password"
}
```

### Login Response

```json
{
  "token": "JWT_TOKEN",
  "user_id": "11111111-1111-1111-1111-111111111111",
  "email": "creator@example.com",
  "name": "Creator Name"
}
```

### Authenticated Request Header

```http
Authorization: Bearer JWT_TOKEN
```

### Create Profile

```json
{
  "id": "22222222-2222-2222-2222-222222222444",
  "profile_name": "AI Founder LinkedIn Profile",
  "niche": "AI automation for founders",
  "offer": "AI marketing workflows and systems",
  "target_audience": "early-stage founders struggling with marketing",
  "expertise": "ML engineer building AI agents",
  "personal_touch": "I used to build these workflows manually before automating them.",
  "market_scope": "global",
  "primary_market": "English-speaking founders online",
  "currency": "USD",
  "locale_notes": "Write in English. Use global SaaS examples and avoid city-specific references unless provided.",
  "tone": "bold, practical",
  "goal": "generate leads"
}
```

### Create Profile Response

```json
{
  "status": "profile created + audience analyzed + ideas created",
  "profile_id": "22222222-2222-2222-2222-222222222444"
}
```

### Get My Profiles Response

```json
[
  {
    "id": "22222222-2222-2222-2222-222222222444",
    "profile_name": "AI Founder LinkedIn Profile",
    "niche": "AI automation for founders",
    "goal": "generate leads"
  }
]
```

### Generate Post

Post format is inferred from the selected content idea's `post_format`.
Use `instagram_content_type` only when `platform` is `instagram`.
Allowed `post_goal` values are `comment`, `dm_keyword`, `follow`, `download`, `share`, `save`, `book_visit`, and `buy_order`.
Allowed `post_length` values are `short`, `medium`, and `long`.
Use `automation_resource_id` only for Instagram posts when the CTA should reuse a saved DM resource.
Use `extra_context` when the user wants this draft to follow a more specific direction than the selected idea alone.

```json
{
  "content_idea_id": "CONTENT_IDEA_UUID",
  "platform": "instagram",
  "instagram_content_type": "carousel",
  "post_goal": "share",
  "post_length": "medium",
  "automation_resource_id": "55555555-5555-5555-5555-555555555555",
  "extra_context": "Mention yesterday's gallery opening and make the CTA softer."
}
```

### Generate Post Response

```json
{
  "status": "post generated",
  "post_id": "33333333-3333-3333-3333-333333333333",
  "post": {
    "hook": "Most founders do not need more content ideas.",
    "body": "They need a repeatable system for turning expertise into useful posts.",
    "cta": "Comment SYSTEM and I will send you the workflow.",
    "final_text": "Most founders do not need more content ideas.\n\nThey need a repeatable system for turning expertise into useful posts.\n\nComment SYSTEM and I will send you the workflow.",
    "automation_resource_id": "55555555-5555-5555-5555-555555555555"
  }
}
```

### Revise Generated Post

`PUT /posts/{post_id}/revise`

```json
{
  "instruction": "Make it shorter, warmer, and less salesy."
}
```

### Get Attached Automation Setup Response

```json
{
  "trigger_keyword": "SYSTEM",
  "public_comment_reply_options": [
    "Sent it to you. Check your DMs.",
    "Just sent it your way.",
    "Thanks for commenting — I sent the workflow."
  ],
  "public_comment_reply": "Sent it to you.",
  "first_message": "Hey there! Thanks for your interest.\n\nClick below and I’ll send the workflow in just a sec.",
  "opening_dm_button_label": "Send me the link",
  "link_button_label": "Open",
  "qualification_question": "Are you building this for yourself or for clients?",
  "follow_up": "Start with the simple version first, then automate the repeatable parts.",
  "automation_resource_id": "55555555-5555-5555-5555-555555555555",
  "automation_resource_title": "Workflow guide",
  "manychat_setup": {
    "manual_required": true,
    "comment_trigger_mode": "specific_word",
    "trigger_keyword": "SYSTEM",
    "public_comment_reply": "Sent it to you.",
    "public_comment_reply_options": [
      "Sent it to you. Check your DMs.",
      "Just sent it your way.",
      "Thanks for commenting — I sent the workflow."
    ],
    "opening_dm_text": "Hey there! Thanks for your interest.\n\nClick below and I’ll send the workflow in just a sec.",
    "opening_dm_button_label": "Send me the link",
    "link_button_label": "Open",
    "flow_type": "instagram_comment_to_dm",
    "resource_used": true,
    "automation_resource_url": "https://example.com/guide",
    "setup_steps": [
      "Create an Instagram Comments automation in ManyChat.",
      "Set the comment trigger to a specific word or reaction.",
      "Use the trigger keyword 'SYSTEM'.",
      "Turn on public comment reply and use: Sent it to you.",
      "Add this opening DM text: Hey there! Thanks for your interest.\n\nClick below and I’ll send the workflow in just a sec.",
      "Set the opening DM button label to: Send me the link",
      "After the button click, add a link step with URL https://example.com/guide and button label: Open",
      "Preview the Comments and DM tabs before going live.",
      "Click Go Live in ManyChat when ready."
    ],
    "api_supported_parts": [
      "Account metadata",
      "Tags and custom fields",
      "Sending content or flows to existing contacts"
    ]
  }
}
```

### Update Post Manually

`PUT /posts/{post_id}`

```json
{
  "hook": "Updated hook",
  "body": "Updated body copy.",
  "cta": "Updated CTA.",
  "final_text": "Updated hook\n\nUpdated body copy.\n\nUpdated CTA."
}
```

---

## Authorization and Security Notes

Authentication uses JWT bearer tokens. `/auth/register` and `/auth/login` return a token, and protected endpoints require that token in the `Authorization` header.

Passwords are hashed with bcrypt before storage. The app never returns password hashes from the API.

Profile ownership is enforced on profile-level endpoints. A signed-in user can only load, update, list posts for, or read generated audience/content data for profiles owned by their user account.

Post ownership is enforced through the post's parent marketing profile. A signed-in user cannot generate a post from another user's content idea, read another user's post, delete another user's post, or create/read automation setups for another user's post. Automation setups are limited to Instagram posts.

Sign out is client-side because JWTs are stateless. The frontend removes the saved token and profile id from browser storage. Tokens expire after 7 days.

Production hardening still needed:

* Set `FRONTEND_ORIGINS` to the deployed frontend origin.
* Use a strong `JWT_SECRET_KEY` from a secrets manager.
* Consider refresh tokens or server-side token revocation.
* Return consistent `404` / `403` responses for missing versus unauthorized resources.
* Expand automated tests around complete user flows.

---

## Tech Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* Psycopg
* Pydantic

### AI

* OpenAI
* LangChain
* ChromaDB
* RAG (Retrieval-Augmented Generation)

### Marketing Automation

* ManyChat (planned integration)

---

## Current MVP Flow

```text
POST /auth/register
        │
        ▼
Create Account + Receive JWT
        │
        ▼
POST /auth/login
        │
        ▼
Sign In + Receive JWT
        │
        ▼
Authenticated Requests

GET /users/me/profiles
        │
        ▼
Select Marketing Profile

POST /user-profiles
        │
        ▼
Audience Agent
        │
        ▼
Audience Analysis
        │
        ▼
Idea Agent
        │
        ▼
Content Ideas

User adds DM resource
        │
        ▼
Automation Agent
        │
        ▼
Reusable Automation Setup

User selects content idea
        │
        ▼
POST /posts
        │
        ▼
Content Agent
        │
        ▼
Generated Post
```

---

## Future Improvements

* Competitor analysis to collect inspiration from relevant social profiles and identify reusable patterns.
* Better model routing for different agents, so high-impact writing can use stronger models while simpler structured tasks stay cheaper.
* Reel storyboard generation for turning posts into short-form video plans.
* Story-to-DM automations and more ManyChat automation types beyond Instagram comment-to-DM.
* More relevant RAG documents, including stronger hook libraries, examples of super popular posts, CTA patterns, and niche-specific content references.
* Additional specialist agents, such as a bio generator, profile optimizer, content calendar planner, or offer positioning assistant.
* Image upload and visual analysis, so the app can suggest content ideas from screenshots, product photos, event photos, or favorite post examples.
* Chatbot-style assistant for asking questions about the profile, audience notes, ideas, posts, and automations.
* Real-time trend analysis and trend-aware content suggestions.
* Multi-platform optimization, automated publishing, scheduled content creation, analytics, and post performance tracking.
