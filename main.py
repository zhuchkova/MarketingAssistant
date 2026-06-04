# uvicorn main:app --reload
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import psycopg
from agents.audience_agent import run_audience_agent
from db.audience_repository import save_audience_analysis
from agents.idea_agent import run_idea_agent
from db.idea_repository import (get_profile_with_audience_analysis,
                                save_content_ideas)
from agents.content_agent import run_content_agent
from db.content_repository import (
    get_content_generation_context,
    get_lookup_id,
    save_post)


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

app = FastAPI()

@app.post("/user-profiles")
def create_profile(profile: dict):
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


@app.post("/posts/generate")
def generate_post(request: dict):
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
#
# {
#   "id": "22222222-2222-2222-2222-222222222444",
#   "user_id": "11111111-1111-1111-1111-111111111111",
#   "niche": "AI automation for founders",
#   "offer": "AI marketing workflows and systems",
#   "target_audience": "early-stage founders struggling with marketing",
#   "expertise": "ML engineer building AI agents",
#   "tone": "bold, practical",
#   "goal": "generate leads"
# }


# {
#   "content_idea_id": "CONTENT_IDEA_UUID",
#   "platform": "linkedin",
#   "post_format": "contrarian",
#   "post_goal": "comment"
# }
