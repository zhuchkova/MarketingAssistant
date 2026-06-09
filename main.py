# uvicorn main:app --reload
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from schemas.user_profile import CreateUserProfileRequest, UpdateUserProfileRequest
from schemas.post_generation import GeneratePostRequest
from agents.audience_agent import run_audience_agent
from db.audience_repository import save_audience_analysis
from agents.idea_agent import run_idea_agent
from db.idea_repository import (get_profile_with_audience_analysis,
                                save_content_ideas)
from agents.content_agent import run_content_agent
from db.content_repository import (get_content_generation_context,
    get_lookup_id, save_post)
from agents.conversion_agent import run_conversion_agent
from db.conversion_repository import (get_conversion_context,
    save_manychat_flow)


def handle_new_profile(conn, profile):
    # 1. run audience agent
    audience_result = run_audience_agent(profile)

    # 2. save audience analysis
    save_audience_analysis(conn, profile["id"], audience_result)

    # 3. get saved profile + audience analysis
    saved_profile, saved_audience_analysis = get_profile_with_audience_analysis(
        conn,
        profile["id"]
    )

    # 4. run idea agent
    ideas = run_idea_agent(
        saved_profile,
        saved_audience_analysis,
        number_of_ideas=10
    )

    # 5. save ideas
    save_content_ideas(
        conn,
        user_profile_id=profile["id"],
        audience_analysis_id=saved_audience_analysis["id"],
        ideas=ideas
    )

    conn.commit()


def regenerate_profile_outputs(conn, profile):
    """Helper function to update profiles"""
    audience_result = run_audience_agent(profile)

    save_audience_analysis(conn, profile["id"], audience_result)

    saved_profile, saved_audience_analysis = get_profile_with_audience_analysis(
        conn,
        profile["id"]
    )

    ideas = run_idea_agent(
        saved_profile,
        saved_audience_analysis,
        number_of_ideas=10
    )

    save_content_ideas(
        conn,
        user_profile_id=profile["id"],
        audience_analysis_id=saved_audience_analysis["id"],
        ideas=ideas
    )

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.post("/user-profiles")
def create_profile(profile: CreateUserProfileRequest):
    profile = profile.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_profiles (
                id, user_id, niche, offer, target_audience, expertise, tone, goal
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            profile["id"],
            profile["user_id"],
            profile["niche"],
            profile["offer"],
            profile["target_audience"],
            profile["expertise"],
            profile["tone"],
            profile["goal"]
        ))

    # trigger agent automatically
    handle_new_profile(conn, profile)

    return {"status": "profile created + audience analyzed + ideas created"}


@app.post("/posts")
def generate_post(request: GeneratePostRequest):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    context = get_content_generation_context(
        conn,
        request["content_idea_id"]
    )

    platform_id = get_lookup_id(conn, "platforms", request["platform"])
    post_format_id = get_lookup_id(conn, "post_formats", request["post_format"])
    post_goal_id = get_lookup_id(conn, "post_goals", request["post_goal"])

    agent_input = {
        **context,
        "platform": request["platform"],
        "post_format": request["post_format"],
        "post_goal": request["post_goal"],
    }

    generated_post = run_content_agent(agent_input)

    post_data = {
        **context,
        **generated_post,
        "platform_id": platform_id,
        "post_format_id": post_format_id,
        "post_goal_id": post_goal_id,
    }

    post_id = save_post(conn, post_data)

    conn.commit()
    conn.close()

    return {
        "status": "post generated",
        "post_id": post_id,
        "post": generated_post,
    }

@app.get("/user-profiles/{profile_id}")
def get_user_profile(profile_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, user_id, niche, offer, target_audience, expertise, tone, goal
            FROM user_profiles
            WHERE id = %s
        """, (profile_id,))

        row = cur.fetchone()

    conn.close()

    if not row:
        return {"error": "Profile not found"}

    return {
        "id": row[0],
        "user_id": row[1],
        "niche": row[2],
        "offer": row[3],
        "target_audience": row[4],
        "expertise": row[5],
        "tone": row[6],
        "goal": row[7],
    }

@app.get("/user-profiles/{profile_id}/audience-analysis")
def get_audience_analysis(profile_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, audience_profile, pains, desires, objections,
                   content_angles, tone, positioning, known_for
            FROM audience_analyses
            WHERE user_profile_id = %s
        """, (profile_id,))

        row = cur.fetchone()

    conn.close()

    if not row:
        return {"error": "Audience analysis not found"}

    return {
        "id": row[0],
        "audience_profile": row[1],
        "pains": row[2],
        "desires": row[3],
        "objections": row[4],
        "content_angles": row[5],
        "tone": row[6],
        "positioning": row[7],
        "known_for": row[8],
    }

@app.get("/user-profiles/{profile_id}/content-ideas")
def get_content_ideas(profile_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, hook, angle, topic
            FROM content_ideas
            WHERE user_profile_id = %s
        """, (profile_id,))

        rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "hook": row[2],
            "angle": row[3],
            "topic": row[4],
        }
        for row in rows
    ]

@app.get("/posts/{post_id}")
def get_post(post_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                p.id,
                p.hook,
                p.body,
                p.cta,
                p.final_text,
                pl.name AS platform,
                pf.name AS post_format,
                pg.name AS post_goal
            FROM posts p
            JOIN platforms pl ON p.platform_id = pl.id
            LEFT JOIN post_formats pf ON p.post_format_id = pf.id
            LEFT JOIN post_goals pg ON p.post_goal_id = pg.id
            WHERE p.id = %s
        """, (post_id,))

        row = cur.fetchone()

    conn.close()

    if not row:
        return {"error": "Post not found"}

    return {
        "id": row[0],
        "hook": row[1],
        "body": row[2],
        "cta": row[3],
        "final_text": row[4],
        "platform": row[5],
        "post_format": row[6],
        "post_goal": row[7],
    }

@app.get("/user-profiles/{profile_id}/posts")
def get_posts_for_profile(profile_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                p.id,
                p.hook,
                p.cta,
                p.final_text,
                pl.name AS platform,
                pf.name AS post_format,
                pg.name AS post_goal
            FROM posts p
            JOIN platforms pl ON p.platform_id = pl.id
            LEFT JOIN post_formats pf ON p.post_format_id = pf.id
            LEFT JOIN post_goals pg ON p.post_goal_id = pg.id
            WHERE p.user_profile_id = %s
        """, (profile_id,))

        rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "hook": row[1],
            "cta": row[2],
            "final_text": row[3],
            "platform": row[4],
            "post_format": row[5],
            "post_goal": row[6],
        }
        for row in rows
    ]

@app.delete("/posts/{post_id}")
def delete_post(post_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM posts
            WHERE id = %s
        """, (post_id,))

    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "post_id": post_id
    }

# PUT /user-profiles/{profile_id}
# → update profile
# → delete old audience analysis + ideas + posts
# → regenerate audience analysis
# → regenerate content ideas

@app.put("/user-profiles/{profile_id}")
def update_user_profile(profile_id: str, request: UpdateUserProfileRequest):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    try:
        with conn.cursor() as cur:
            # 1. Check profile exists and get user_id
            cur.execute("""
                SELECT user_id
                FROM user_profiles
                WHERE id = %s
            """, (profile_id,))

            row = cur.fetchone()

            if not row:
                raise HTTPException(status_code=404, detail="Profile not found")

            user_id = row[0]

            # 2. Delete generated old data
            # Alternatively, we could add ON DELETE CASCADE to FKs, then deleting audience_analyses
            # would already delete content_ideas, depending on the schema.
            cur.execute("""
                DELETE FROM posts
                WHERE user_profile_id = %s
            """, (profile_id,))

            cur.execute("""
                DELETE FROM content_ideas
                WHERE user_profile_id = %s
            """, (profile_id,))

            cur.execute("""
                DELETE FROM audience_analyses
                WHERE user_profile_id = %s
            """, (profile_id,))

            # 3. Update profile input
            cur.execute("""
                UPDATE user_profiles
                SET
                    niche = %s,
                    offer = %s,
                    target_audience = %s,
                    expertise = %s,
                    tone = %s,
                    goal = %s
                WHERE id = %s
            """, (
                request["niche"],
                request["offer"],
                request["target_audience"],
                request["expertise"],
                request["tone"],
                request["goal"],
                profile_id,
            ))

        # 4. Build profile dict for agents
        profile = {
            "id": profile_id,
            "user_id": user_id,
            "niche": request["niche"],
            "offer": request["offer"],
            "target_audience": request["target_audience"],
            "expertise": request["expertise"],
            "tone": request["tone"],
            "goal": request["goal"],
        }

        # 5. Regenerate AI outputs
        regenerate_profile_outputs(conn, profile)

        conn.commit()

        return {
            "status": "profile updated + audience analysis and ideas regenerated",
            "profile_id": profile_id
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


@app.post("/posts/{post_id}/conversion")
def create_conversion_flow(post_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    try:
        context = get_conversion_context(conn, post_id)

        flow = run_conversion_agent(context)

        flow_id = save_manychat_flow(conn, post_id, flow)

        conn.commit()

        return {
            "status": "conversion flow created",
            "flow_id": flow_id,
            "post_id": post_id,
            "flow": flow,
        }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


@app.get("/posts/{post_id}/conversion")
def get_conversion_flow(post_id: str):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                trigger_keyword,
                first_message,
                qualification_question,
                follow_up
            FROM manychat_flows
            WHERE post_id = %s
        """, (post_id,))

        row = cur.fetchone()

    conn.close()

    if not row:
        return {"error": "Conversion flow not found"}

    return {
        "id": row[0],
        "trigger_keyword": row[1],
        "first_message": row[2],
        "qualification_question": row[3],
        "follow_up": row[4],
    }


app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

