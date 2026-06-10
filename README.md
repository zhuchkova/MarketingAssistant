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
* Generate conversion funnels and ManyChat automations

The goal is to provide highly relevant, engaging, and conversion-oriented content rather than generic AI-generated posts.

Each user can manage multiple marketing profiles (for example: LinkedIn Personal Brand, AI Consulting Business, Fitness Coaching Brand), each with its own audience analysis, content ideas, posts, and conversion funnels.

---

## Architecture

```text
User
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
* Angle
* Topic

---

### 3. Content Agent

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

Creates ManyChat conversion flows from generated posts.

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
user_profiles
  ├── profile_name
  ├── niche
  ├── offer
  ├── target_audience
  ├── expertise
  ├── tone
  └── goal

audience_analyses
content_ideas
posts
manychat_flows
```

### ChromaDB

Stores marketing knowledge used by RAG agents.

---

## API Endpoints

### Users

#### Get All Users

```http
GET /users
```

#### Get User Profiles

```http
GET /users/{user_id}/profiles
```

Returns all marketing profiles belonging to a user.

---

### Profiles

#### Create Profile

```http
POST /user-profiles
```

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

#### Delete Post

```http
DELETE /posts/{post_id}
```

---

### Conversion

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

### Create Profile

```json
{
  "id": "22222222-2222-2222-2222-222222222444",
  "user_id": "11111111-1111-1111-1111-111111111111",
  "profile_name": "AI Founder LinkedIn Profile",
  "niche": "AI automation for founders",
  "offer": "AI marketing workflows and systems",
  "target_audience": "early-stage founders struggling with marketing",
  "expertise": "ML engineer building AI agents",
  "tone": "bold, practical",
  "goal": "generate leads"
}
```

### Generate Post

```json
{
  "content_idea_id": "CONTENT_IDEA_UUID",
  "platform": "linkedin",
  "post_format": "contrarian",
  "post_goal": "comment"
}
```

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
GET /users
        │
        ▼
Select User

GET /users/{user_id}/profiles
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

* User authentication and authorization
* Real-time trend analysis
* Multi-platform optimization
* ManyChat API integration
* Automated publishing
* Agent orchestration with LangGraph
* Analytics and post performance tracking
* A/B testing of hooks and CTAs
* Content calendar generation
* Scheduled content creation and publishing

```
```
