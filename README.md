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
Conversion Agent
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

Generates complete LinkedIn or Instagram posts.

#### Input

* Content Idea
* Platform
* Format
* Goal

#### Output

* Hook
* Body
* CTA
* Final Post

---

### 4. Conversion Agent

Creates ManyChat-style conversion flows from generated Instagram posts.

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

### cta_conversion_knowledge

Used by the Conversion Agent.

Contains:

* CTA best practices
* Lead magnet strategies
* Comment-to-DM patterns

---

### manychat_funnel_templates

Used by the Conversion Agent.

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
  ├── post_format
  └── is_favorite
posts
  ├── instagram_content_type
  ├── post_length
  ├── is_favorite
  ├── is_published
  ├── published_at
  ├── hook
  ├── body
  ├── cta
  └── final_text
lead_magnets
  ├── title
  ├── url
  ├── description
  ├── suggested_keyword
  ├── delivery_message
  ├── follow_up_cta
  └── is_primary
manychat_flows
  ├── lead_magnet_id
  ├── trigger_keyword
  ├── public_comment_reply
  ├── first_message
  ├── qualification_question
  ├── follow_up
  └── manychat_setup
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
```

`DATABASE_URL` is required by FastAPI endpoints and `scripts/migrate.py`.

`JWT_SECRET_KEY` signs login tokens and is required. The API will reject token operations if this is missing.

`OPENAI_API_KEY` is required by the LangChain/OpenAI agents. The agents currently use `openai:gpt-4o-mini` through `init_chat_model`.

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
* `cta_conversion_knowledge.json` for comment, DM, save, follow, download, share, book/visit, buy/order, public reply, and no-guide fallback CTA patterns.
* `manychat_funnel_templates.json` for keyword flows, public comment replies, first messages, qualifying questions, follow-ups, lead magnet delivery, no-guide fallbacks, and manual ManyChat setup JSON.

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

### Conversion

Lead flow setup is optional and happens after the main profile workflow. A user can create a profile, review audience analysis, generate ideas, and draft posts without adding any lead magnet or ManyChat resource.

In the frontend, reusable flow resources are managed from the **Lead Flows** dashboard tab. These resources are used only for Instagram comment-to-DM flows. LinkedIn posts and Instagram stories can still be drafted without conversion flows.

#### Profile Lead Magnets

```http
GET /user-profiles/{profile_id}/lead-magnets
POST /user-profiles/{profile_id}/lead-magnets
PUT /user-profiles/{profile_id}/lead-magnets/{lead_magnet_id}
DELETE /user-profiles/{profile_id}/lead-magnets/{lead_magnet_id}
```

Lead magnets are optional reusable guides/resources for Instagram comment-to-DM flows. If no lead magnet exists, the app can still generate a goal-based flow such as booking details, order details, or a simple first-step conversation.

#### Generate Conversion Flow

```http
POST /posts/{post_id}/conversion
```

Triggers:

```text
Conversion Agent
```

#### Get Conversion Flow

```http
GET /posts/{post_id}/conversion
```

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

```json
{
  "content_idea_id": "CONTENT_IDEA_UUID",
  "platform": "instagram",
  "instagram_content_type": "carousel",
  "post_goal": "share",
  "post_length": "medium"
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
    "final_text": "Most founders do not need more content ideas.\n\nThey need a repeatable system for turning expertise into useful posts.\n\nComment SYSTEM and I will send you the workflow."
  }
}
```

### Generate Conversion Flow Response

Optional request body:

```json
{
  "lead_magnet_id": "55555555-5555-5555-5555-555555555555",
  "custom_offer_title": null,
  "custom_offer_url": null,
  "custom_offer_description": null
}
```

```json
{
  "status": "conversion flow created",
  "flow_id": "44444444-4444-4444-4444-444444444444",
  "post_id": "33333333-3333-3333-3333-333333333333",
  "flow": {
    "trigger_keyword": "SYSTEM",
    "public_comment_reply": "Sent it to you.",
    "first_message": "Here is the workflow I mentioned.",
    "qualification_question": "Are you building this for yourself or for clients?",
    "follow_up": "Start with the simple version first, then automate the repeatable parts.",
    "manychat_setup": {
      "manual_required": true,
      "trigger_keyword": "SYSTEM",
      "public_comment_reply": "Sent it to you.",
      "flow_type": "instagram_comment_to_dm",
      "lead_magnet_used": true,
      "lead_magnet_url": "https://example.com/guide",
      "setup_steps": [
        "Create an Instagram Comments automation in ManyChat.",
        "Use SYSTEM as the trigger keyword.",
        "Add the public reply and DM messages from this flow."
      ],
      "api_supported_parts": ["tags", "custom_fields", "sendContent", "sendFlow"]
    }
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

Post ownership is enforced through the post's parent marketing profile. A signed-in user cannot generate a post from another user's content idea, read another user's post, delete another user's post, or create/read conversion flows for another user's post. Conversion flows are limited to Instagram posts.

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

POST /posts/{post_id}/conversion
        │
        ▼
Conversion Agent
        │
        ▼
ManyChat Flow
```

---

## Future Improvements

* Server-side token revocation or refresh tokens
* Real-time trend analysis
* Multi-platform optimization
* ManyChat API integration
* Automated publishing
* Agent orchestration with LangGraph
* Analytics and post performance tracking
* A/B testing of hooks and CTAs
* Content calendar generation
* Scheduled content creation and publishing
