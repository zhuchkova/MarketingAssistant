# uvicorn main:app --reload
import os
import uuid
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from schemas.user_profile import CreateUserProfileRequest, UpdateUserProfileRequest
from schemas.post_generation import GeneratePostRequest, UpdatePostRequest
from schemas.content_idea import ContentIdeaRequest, GenerateIdeasRequest
from schemas.automation_resource import AutomationResourceRequest
from schemas.auth import RegisterRequest, LoginRequest
from auth import get_current_user, hash_password, verify_password, create_token
from authorization import check_profile_owner, check_post_owner
from agents.audience_agent import run_audience_agent
from db.audience_repository import save_audience_analysis
from agents.idea_agent import run_idea_agent
from db.idea_repository import (get_profile_with_audience_analysis,
                                save_content_ideas)
from agents.content_agent import run_content_agent
from db.content_repository import (get_content_generation_context,
    get_lookup_id, save_post, update_post_content)
from agents.automation_agent import run_automation_agent
from db.automation_context_repository import (get_automation_context,
    attach_automation_resource_context)
from db.manychat_setup_builder import flow_from_automation_resource
from db.automation_resource_repository import (
    delete_automation_resource,
    get_automation_resource,
    list_automation_resources,
    save_automation_resource,
    update_automation_resource,
    update_automation_resource_setup,
)


def get_allowed_origins() -> List[str]:
    origins = os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000,http://127.0.0.1:3000,http://localhost:3000",
    )
    return [origin.strip() for origin in origins.split(",") if origin.strip()]


def handle_new_profile(conn, profile):
    audience_result = run_audience_agent(profile)
    save_audience_analysis(conn, profile["id"], audience_result)
    saved_profile, saved_audience_analysis = get_profile_with_audience_analysis(
        conn, profile["id"]
    )
    ideas = run_idea_agent(saved_profile, saved_audience_analysis, number_of_ideas=20)
    save_content_ideas(
        conn,
        user_profile_id=profile["id"],
        audience_analysis_id=saved_audience_analysis["id"],
        ideas=ideas
    )
    conn.commit()


def regenerate_profile_outputs(conn, profile):
    audience_result = run_audience_agent(profile)
    save_audience_analysis(conn, profile["id"], audience_result)
    saved_profile, saved_audience_analysis = get_profile_with_audience_analysis(
        conn, profile["id"]
    )
    ideas = run_idea_agent(saved_profile, saved_audience_analysis, number_of_ideas=20)
    save_content_ideas(
        conn,
        user_profile_id=profile["id"],
        audience_analysis_id=saved_audience_analysis["id"],
        ideas=ideas
    )


def ensure_content_idea_owner(conn, idea_id: str, user_id: str) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                ci.id,
                ci.user_profile_id,
                ci.audience_analysis_id,
                ci.title,
                ci.hook,
                ci.angle,
                ci.topic,
                COALESCE(ci.post_format, ci.content_style) AS post_format
            FROM content_ideas ci
            JOIN user_profiles up ON ci.user_profile_id = up.id
            WHERE ci.id = %s AND up.user_id = %s
        """, (idea_id, user_id))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Content idea not found")

    return {
        "id": row[0],
        "user_profile_id": row[1],
        "audience_analysis_id": row[2],
        "title": row[3],
        "hook": row[4],
        "angle": row[5],
        "topic": row[6],
        "post_format": row[7],
    }


def get_profile_and_audience_for_generation(conn, profile_id: str, user_id: str) -> tuple:
    check_profile_owner(conn, profile_id, user_id)
    try:
        return get_profile_with_audience_analysis(conn, profile_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Audience analysis is missing for this profile")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_ui():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "static", "index.html"),
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


# ── AUTH ──────────────────────────────────────────────

@app.post("/auth/register")
def register(request: RegisterRequest):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (request.email,))
            if cur.fetchone():
                raise HTTPException(status_code=409, detail="Email already registered")
            user_id = str(uuid.uuid4())
            hashed = hash_password(request.password)
            cur.execute(
                "INSERT INTO users (id, email, name, hashed_password) VALUES (%s, %s, %s, %s)",
                (user_id, request.email, request.name, hashed),
            )
        token = create_token(user_id, request.email, request.name)
        conn.commit()
        return {"token": token, "user_id": user_id, "email": request.email, "name": request.name}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.post("/auth/login")
def login(request: LoginRequest):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, hashed_password, name FROM users WHERE email = %s",
                (request.email,),
            )
            row = cur.fetchone()
        if not row or not row[1] or not verify_password(request.password, row[1]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        name = row[2] or ""
        token = create_token(str(row[0]), request.email, name)
        return {"token": token, "user_id": str(row[0]), "email": request.email, "name": name}
    finally:
        conn.close()


# ── USER PROFILES ─────────────────────────────────────

@app.post("/user-profiles")
def create_profile(
    profile: CreateUserProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    profile = profile.model_dump()
    profile["id"] = profile.get("id") or str(uuid.uuid4())
    profile["user_id"] = current_user["user_id"]

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_profiles (
                    id, user_id, profile_name, niche, offer, target_audience, expertise, personal_touch,
                    market_scope, primary_market, currency, locale_notes, tone, goal
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                profile["id"],
                profile["user_id"],
                profile["profile_name"],
                profile["niche"],
                profile["offer"],
                profile["target_audience"],
                profile["expertise"],
                profile.get("personal_touch"),
                profile.get("market_scope"),
                profile.get("primary_market"),
                profile.get("currency"),
                profile.get("locale_notes"),
                profile["tone"],
                profile["goal"]
            ))

        handle_new_profile(conn, profile)

        return {"status": "profile created + audience analyzed + ideas created", "profile_id": profile["id"]}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.get("/users/me/profiles")
def get_my_profiles(current_user: dict = Depends(get_current_user)):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, profile_name, niche, goal
                FROM user_profiles
                WHERE user_id = %s
                ORDER BY profile_name
            """, (current_user["user_id"],))
            rows = cur.fetchall()
        return [
            {"id": row[0], "profile_name": row[1], "niche": row[2], "goal": row[3]}
            for row in rows
        ]
    finally:
        conn.close()


@app.get("/user-profiles/{profile_id}")
def get_user_profile(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, user_id, profile_name, niche, offer, target_audience, expertise, personal_touch,
                       market_scope, primary_market, currency, locale_notes, tone, goal
                FROM user_profiles
                WHERE id = %s
            """, (profile_id,))
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return {"error": "Profile not found"}
    if str(row[1]) != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "id": row[0],
        "user_id": row[1],
        "profile_name": row[2],
        "niche": row[3],
        "offer": row[4],
        "target_audience": row[5],
        "expertise": row[6],
        "personal_touch": row[7],
        "market_scope": row[8],
        "primary_market": row[9],
        "currency": row[10],
        "locale_notes": row[11],
        "tone": row[12],
        "goal": row[13],
    }


@app.get("/user-profiles/{profile_id}/audience-analysis")
def get_audience_analysis(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, audience_profile, pains, desires, objections,
                       trigger_moments, proof_points, audience_language,
                       market_context, content_angles, tone, positioning, known_for
                FROM audience_analyses
                WHERE user_profile_id = %s
            """, (profile_id,))
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return {"error": "Audience analysis not found"}

    return {
        "id": row[0],
        "audience_profile": row[1],
        "pains": row[2],
        "desires": row[3],
        "objections": row[4],
        "trigger_moments": row[5],
        "proof_points": row[6],
        "audience_language": row[7],
        "market_context": row[8],
        "content_angles": row[9],
        "tone": row[10],
        "positioning": row[11],
        "known_for": row[12],
    }


def get_automation_resource_generation_context(conn, profile_id: str, automation_resource: dict) -> dict:
    profile, audience_analysis = get_profile_with_audience_analysis(conn, profile_id)
    if not profile or not audience_analysis:
        raise ValueError("Profile or audience analysis not found")

    context = {
        **profile,
        **audience_analysis,
        "audience_analysis_id": audience_analysis.get("id"),
        "post_id": None,
        "platform": "instagram",
        "post_goal": automation_resource.get("preferred_post_goal") or "dm_keyword",
        "hook": "",
        "body": "",
        "cta": "",
        "final_text": (
            "Reusable Instagram comment-to-DM automation resource. "
            "Generate keyword, public reply, opening DM, button labels, "
            "optional qualification question, follow-up, and setup JSON."
        ),
    }
    return attach_automation_resource_context(context, automation_resource=automation_resource)


@app.get("/user-profiles/{profile_id}/lead-magnets", include_in_schema=False)
@app.get("/user-profiles/{profile_id}/automation-resources")
def get_profile_automation_resources(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        return list_automation_resources(conn, profile_id)
    finally:
        conn.close()


@app.post("/user-profiles/{profile_id}/lead-magnets", include_in_schema=False)
@app.post("/user-profiles/{profile_id}/automation-resources")
def create_profile_automation_resource(
    profile_id: str,
    request: AutomationResourceRequest,
    current_user: dict = Depends(get_current_user),
):
    data = request.model_dump()
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        is_primary = len(list_automation_resources(conn, profile_id)) == 0
        automation_resource_id = save_automation_resource(conn, profile_id, data, is_primary=is_primary)
        conn.commit()
        return {
            "status": "automation resource created",
            "automation_resource_id": automation_resource_id,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.put("/user-profiles/{profile_id}/lead-magnets/{automation_resource_id}", include_in_schema=False)
@app.put("/user-profiles/{profile_id}/automation-resources/{automation_resource_id}")
def update_profile_automation_resource(
    profile_id: str,
    automation_resource_id: str,
    request: AutomationResourceRequest,
    current_user: dict = Depends(get_current_user),
):
    data = request.model_dump()
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        update_automation_resource(conn, automation_resource_id, profile_id, data)
        conn.commit()
        return {
            "status": "automation resource updated",
            "automation_resource_id": automation_resource_id,
        }
    except ValueError:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Automation resource not found")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.post("/user-profiles/{profile_id}/lead-magnets/{automation_resource_id}/generate-flow", include_in_schema=False)
@app.post("/user-profiles/{profile_id}/automation-resources/{automation_resource_id}/generate-automation")
def generate_profile_automation_resource_setup(
    profile_id: str,
    automation_resource_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        try:
            automation_resource = get_automation_resource(conn, automation_resource_id, profile_id)
            context = get_automation_resource_generation_context(conn, profile_id, automation_resource)
        except ValueError as exc:
            raise HTTPException(status_code=404, detail=str(exc))

        flow = run_automation_agent(context)
        update_automation_resource_setup(conn, automation_resource_id, profile_id, flow)
        conn.commit()
        return {
            "status": "automation generated",
            "automation_resource_id": automation_resource_id,
            "flow": flow,
        }
    except HTTPException:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.post("/user-profiles/{profile_id}/lead-magnets/generate-flows", include_in_schema=False)
@app.post("/user-profiles/{profile_id}/automation-resources/regenerate-automations")
def generate_profile_automation_resource_setups(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    generated = []
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        automation_resources = list_automation_resources(conn, profile_id)
        for automation_resource in automation_resources:
            context = get_automation_resource_generation_context(conn, profile_id, automation_resource)
            flow = run_automation_agent(context)
            update_automation_resource_setup(conn, automation_resource["id"], profile_id, flow)
            generated.append({
                "automation_resource_id": automation_resource["id"],
                "title": automation_resource["title"],
                "flow": flow,
            })

        conn.commit()
        return {
            "status": "automations generated",
            "count": len(generated),
            "flows": generated,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.delete("/user-profiles/{profile_id}/lead-magnets/{automation_resource_id}", include_in_schema=False)
@app.delete("/user-profiles/{profile_id}/automation-resources/{automation_resource_id}")
def delete_profile_automation_resource(
    profile_id: str,
    automation_resource_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])
        delete_automation_resource(conn, automation_resource_id, profile_id)
        conn.commit()
        return {
            "status": "automation resource deleted",
            "automation_resource_id": automation_resource_id,
        }
    except ValueError:
        conn.rollback()
        raise HTTPException(status_code=404, detail="Automation resource not found")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.get("/user-profiles/{profile_id}/content-ideas")
def get_content_ideas(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    title,
                    hook,
                    angle,
                    topic,
                    COALESCE(post_format, content_style) AS post_format,
                    COALESCE(is_favorite, FALSE) AS is_favorite
                FROM content_ideas
                WHERE user_profile_id = %s
                ORDER BY is_favorite DESC, title
            """, (profile_id,))
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "hook": row[2],
            "angle": row[3],
            "topic": row[4],
            "post_format": row[5],
            "is_favorite": row[6],
        }
        for row in rows
    ]


@app.post("/user-profiles/{profile_id}/content-ideas/generate-more")
def generate_more_content_ideas(
    profile_id: str,
    request: GenerateIdeasRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        profile, audience_analysis = get_profile_and_audience_for_generation(
            conn, profile_id, current_user["user_id"]
        )
        ideas = run_idea_agent(profile, audience_analysis, number_of_ideas=request["count"])
        idea_ids = save_content_ideas(
            conn,
            user_profile_id=profile_id,
            audience_analysis_id=audience_analysis["id"],
            ideas=ideas,
        )
        conn.commit()
        return {"status": "ideas added", "idea_ids": idea_ids}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.post("/user-profiles/{profile_id}/content-ideas/regenerate")
def regenerate_content_ideas(
    profile_id: str,
    request: GenerateIdeasRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        profile, audience_analysis = get_profile_and_audience_for_generation(
            conn, profile_id, current_user["user_id"]
        )
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM content_ideas
                WHERE user_profile_id = %s
                  AND COALESCE(is_favorite, FALSE) = FALSE
            """, (profile_id,))

        ideas = run_idea_agent(profile, audience_analysis, number_of_ideas=request["count"])
        idea_ids = save_content_ideas(
            conn,
            user_profile_id=profile_id,
            audience_analysis_id=audience_analysis["id"],
            ideas=ideas,
        )
        conn.commit()
        return {"status": "ideas regenerated", "idea_ids": idea_ids}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.post("/user-profiles/{profile_id}/content-ideas")
def create_custom_content_idea(
    profile_id: str,
    request: ContentIdeaRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        _, audience_analysis = get_profile_and_audience_for_generation(
            conn, profile_id, current_user["user_id"]
        )
        idea_id = str(uuid.uuid4())
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO content_ideas (
                    id, user_profile_id, audience_analysis_id,
                    title, hook, angle, topic, post_format
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                idea_id,
                profile_id,
                audience_analysis["id"],
                request["title"],
                request["hook"],
                request["angle"],
                request["topic"],
                request["post_format"],
            ))
        conn.commit()
        return {"status": "idea created", "idea_id": idea_id}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.put("/content-ideas/{idea_id}")
def update_content_idea(
    idea_id: str,
    request: ContentIdeaRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        ensure_content_idea_owner(conn, idea_id, current_user["user_id"])
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE content_ideas
                SET title=%s, hook=%s, angle=%s, topic=%s, post_format=%s
                WHERE id=%s
            """, (
                request["title"],
                request["hook"],
                request["angle"],
                request["topic"],
                request["post_format"],
                idea_id,
            ))
        conn.commit()
        return {"status": "idea updated", "idea_id": idea_id}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.put("/content-ideas/{idea_id}/favorite")
def toggle_content_idea_favorite(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        ensure_content_idea_owner(conn, idea_id, current_user["user_id"])
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE content_ideas
                SET is_favorite = NOT COALESCE(is_favorite, FALSE)
                WHERE id = %s
                RETURNING is_favorite
            """, (idea_id,))
            row = cur.fetchone()
        conn.commit()
        return {"status": "idea favorite updated", "idea_id": idea_id, "is_favorite": row[0]}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.delete("/content-ideas/{idea_id}")
def delete_content_idea(
    idea_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        ensure_content_idea_owner(conn, idea_id, current_user["user_id"])
        with conn.cursor() as cur:
            cur.execute("DELETE FROM content_ideas WHERE id = %s", (idea_id,))
        conn.commit()
        return {"status": "idea deleted", "idea_id": idea_id}
    finally:
        conn.close()


@app.get("/user-profiles/{profile_id}/posts")
def get_posts_for_profile(
    profile_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.id, p.hook, p.cta, p.final_text,
                    p.instagram_content_type,
                    p.post_length,
                    COALESCE(p.is_favorite, FALSE) AS is_favorite,
                    COALESCE(p.is_published, FALSE) AS is_published,
                    pl.name AS platform,
                    pf.name AS post_format,
                    pg.name AS post_goal,
                    p.automation_resource_id,
                    ar.title AS automation_resource_title
                FROM posts p
                JOIN platforms pl ON p.platform_id = pl.id
                LEFT JOIN post_formats pf ON p.post_format_id = pf.id
                LEFT JOIN post_goals pg ON p.post_goal_id = pg.id
                LEFT JOIN automation_resources ar ON p.automation_resource_id = ar.id
                WHERE p.user_profile_id = %s
            """, (profile_id,))
            rows = cur.fetchall()
    finally:
        conn.close()

    return [
        {
            "id": row[0], "hook": row[1], "cta": row[2], "final_text": row[3],
            "instagram_content_type": row[4], "post_length": row[5],
            "is_favorite": row[6], "is_published": row[7],
            "platform": row[8], "post_format": row[9], "post_goal": row[10],
            "automation_resource_id": row[11], "automation_resource_title": row[12],
        }
        for row in rows
    ]


@app.put("/user-profiles/{profile_id}")
def update_user_profile(
    profile_id: str,
    request: UpdateUserProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))

    try:
        check_profile_owner(conn, profile_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM content_ideas
                WHERE user_profile_id = %s
                  AND COALESCE(is_favorite, FALSE) = FALSE
            """, (profile_id,))
            cur.execute("""
                UPDATE user_profiles
                SET profile_name=%s, niche=%s, offer=%s, target_audience=%s, expertise=%s, personal_touch=%s,
                    market_scope=%s, primary_market=%s, currency=%s, locale_notes=%s, tone=%s, goal=%s
                WHERE id=%s
            """, (
                request["profile_name"], request["niche"], request["offer"], request["target_audience"],
                request["expertise"], request.get("personal_touch"),
                request.get("market_scope"), request.get("primary_market"), request.get("currency"), request.get("locale_notes"),
                request["tone"], request["goal"], profile_id,
            ))

        profile = {
            "id": profile_id,
            "user_id": current_user["user_id"],
            **request,
        }

        regenerate_profile_outputs(conn, profile)
        conn.commit()

        return {"status": "profile updated + regenerated", "profile_id": profile_id}

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# ── POSTS ─────────────────────────────────────────────

@app.post("/posts")
def generate_post(
    request: GeneratePostRequest,
    current_user: dict = Depends(get_current_user),
):
    request = request.model_dump()

    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        context = get_content_generation_context(conn, request["content_idea_id"])
        check_profile_owner(conn, context["user_profile_id"], current_user["user_id"])
        platform_id = get_lookup_id(conn, "platforms", request["platform"])
        post_format = context.get("idea_post_format") or "how_to"
        post_format_id = get_lookup_id(conn, "post_formats", post_format)
        post_goal_id = get_lookup_id(conn, "post_goals", request["post_goal"])
        automation_resource = None
        if request.get("automation_resource_id"):
            if request["platform"] != "instagram":
                raise HTTPException(
                    status_code=400,
                    detail="DM resources can only be attached to Instagram posts",
                )
            if request.get("instagram_content_type") == "story":
                raise HTTPException(
                    status_code=400,
                    detail="Comment-to-DM automations are only available for Instagram reels and carousels",
                )
            try:
                automation_resource = get_automation_resource(
                    conn,
                    request["automation_resource_id"],
                    context["user_profile_id"],
                )
            except ValueError:
                raise HTTPException(status_code=404, detail="DM resource not found")

        agent_input = {
            **context,
            "platform": request["platform"],
            "instagram_content_type": request.get("instagram_content_type") if request["platform"] == "instagram" else None,
            "post_length": request.get("post_length", "medium"),
            "post_format": post_format,
            "post_goal": request["post_goal"],
            "automation_resource_id": automation_resource["id"] if automation_resource else None,
            "automation_resource_title": automation_resource["title"] if automation_resource else None,
            "automation_resource_url": automation_resource["url"] if automation_resource else None,
            "automation_resource_description": automation_resource["description"] if automation_resource else None,
            "automation_resource_keyword": automation_resource["suggested_keyword"] if automation_resource else None,
            "automation_resource_trigger_type": automation_resource.get("trigger_type") if automation_resource else None,
            "automation_resource_public_comment_reply": automation_resource.get("public_comment_reply") if automation_resource else None,
            "automation_resource_delivery_message": automation_resource["delivery_message"] if automation_resource else None,
            "automation_resource_opening_dm_button_label": automation_resource.get("opening_dm_button_label") if automation_resource else None,
            "automation_resource_link_button_label": automation_resource.get("link_button_label") if automation_resource else None,
            "automation_resource_qualification_question": automation_resource.get("qualification_question") if automation_resource else None,
            "automation_resource_follow_up_cta": automation_resource["follow_up_cta"] if automation_resource else None,
            "automation_resource_preferred_post_goal": automation_resource.get("preferred_post_goal") if automation_resource else None,
        }

        generated_post = run_content_agent(agent_input)

        post_data = {
            **context,
            **generated_post,
            "platform_id": platform_id,
            "post_format_id": post_format_id,
            "post_goal_id": post_goal_id,
            "automation_resource_id": agent_input["automation_resource_id"],
            "instagram_content_type": agent_input["instagram_content_type"],
            "post_length": agent_input["post_length"],
        }

        post_id = save_post(conn, post_data)
        conn.commit()

        return {
            "status": "post generated",
            "post_id": post_id,
            "post": {
                **generated_post,
                "automation_resource_id": agent_input["automation_resource_id"],
                "automation_resource_title": automation_resource["title"] if automation_resource else None,
                "platform": request["platform"],
                "instagram_content_type": agent_input["instagram_content_type"],
                "post_goal": request["post_goal"],
                "post_length": agent_input["post_length"],
            },
        }
    finally:
        conn.close()


@app.get("/posts/{post_id}")
def get_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    p.id, p.hook, p.body, p.cta, p.final_text,
                    p.instagram_content_type,
                    p.post_length,
                    COALESCE(p.is_favorite, FALSE) AS is_favorite,
                    COALESCE(p.is_published, FALSE) AS is_published,
                    pl.name AS platform,
                    pf.name AS post_format,
                    pg.name AS post_goal,
                    p.automation_resource_id,
                    ar.title AS automation_resource_title
                FROM posts p
                JOIN platforms pl ON p.platform_id = pl.id
                LEFT JOIN post_formats pf ON p.post_format_id = pf.id
                LEFT JOIN post_goals pg ON p.post_goal_id = pg.id
                LEFT JOIN automation_resources ar ON p.automation_resource_id = ar.id
                WHERE p.id = %s
            """, (post_id,))
            row = cur.fetchone()
    finally:
        conn.close()

    if not row:
        return {"error": "Post not found"}

    return {
        "id": row[0], "hook": row[1], "body": row[2], "cta": row[3],
        "final_text": row[4], "instagram_content_type": row[5], "post_length": row[6],
        "is_favorite": row[7], "is_published": row[8],
        "platform": row[9], "post_format": row[10], "post_goal": row[11],
        "automation_resource_id": row[12], "automation_resource_title": row[13],
    }


@app.put("/posts/{post_id}")
def update_post(
    post_id: str,
    request: UpdatePostRequest,
    current_user: dict = Depends(get_current_user),
):
    data = request.model_dump()
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])
        update_post_content(conn, post_id, data)
        conn.commit()
        return {"status": "post updated", "post_id": post_id}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.put("/posts/{post_id}/favorite")
def toggle_post_favorite(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE posts
                SET is_favorite = NOT COALESCE(is_favorite, FALSE)
                WHERE id = %s
                RETURNING is_favorite
            """, (post_id,))
            row = cur.fetchone()
        conn.commit()
        return {"status": "post favorite updated", "post_id": post_id, "is_favorite": row[0]}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.put("/posts/{post_id}/published")
def toggle_post_published(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE posts
                SET is_published = NOT COALESCE(is_published, FALSE),
                    published_at = CASE
                        WHEN COALESCE(is_published, FALSE) = FALSE THEN NOW()
                        ELSE NULL
                    END
                WHERE id = %s
                RETURNING is_published
            """, (post_id,))
            row = cur.fetchone()
        conn.commit()
        return {"status": "post published updated", "post_id": post_id, "is_published": row[0]}
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@app.delete("/posts/{post_id}")
def delete_post(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])

        with conn.cursor() as cur:
            cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))

        conn.commit()
    finally:
        conn.close()

    return {"status": "deleted", "post_id": post_id}


@app.get("/posts/{post_id}/conversion", include_in_schema=False)
@app.get("/posts/{post_id}/automation")
def get_post_automation_setup(
    post_id: str,
    current_user: dict = Depends(get_current_user),
):
    conn = psycopg.connect(os.getenv("DATABASE_URL"))
    try:
        check_post_owner(conn, post_id, current_user["user_id"])
        context = get_automation_context(conn, post_id)
        if context.get("platform") != "instagram":
            raise HTTPException(
                status_code=400,
                detail="Comment-to-DM automations are only available for Instagram posts",
            )
        if context.get("instagram_content_type") == "story":
            raise HTTPException(
                status_code=400,
                detail="Comment-to-DM automations are only available for Instagram reels and carousels",
            )

        selected_resource_id = context.get("post_automation_resource_id")
        if not selected_resource_id:
            return {"error": "No prepared automation is attached to this post"}

        try:
            automation_resource = get_automation_resource(
                conn,
                selected_resource_id,
                context["user_profile_id"],
            )
        except ValueError:
            return {"error": "Attached automation resource was not found"}

        return {
            **flow_from_automation_resource(automation_resource),
            "id": None,
            "automation_resource_id": automation_resource["id"],
            "automation_resource_title": automation_resource["title"],
        }
    finally:
        conn.close()


app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
