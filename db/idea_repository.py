import uuid
from typing import Dict, Tuple


def get_profile_with_audience_analysis(conn, profile_id: str) -> Tuple[Dict, Dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                up.id,
                up.user_id,
                up.niche,
                up.offer,
                up.target_audience,
                up.expertise,
                up.personal_touch,
                up.market_scope,
                up.primary_market,
                up.currency,
                up.locale_notes,
                up.tone,
                up.goal,
                aa.id AS audience_analysis_id,
                aa.audience_profile,
                aa.pains,
                aa.desires,
                aa.objections,
                aa.trigger_moments,
                aa.proof_points,
                aa.audience_language,
                aa.market_context,
                aa.content_angles,
                aa.positioning,
                aa.known_for
            FROM user_profiles up
            JOIN audience_analyses aa
                ON aa.user_profile_id = up.id
            WHERE up.id = %s
        """, (profile_id,))

        row = cur.fetchone()

        if not row:
            raise ValueError("No profile with audience analysis found")

        profile = {
            "id": row[0],
            "user_id": row[1],
            "niche": row[2],
            "offer": row[3],
            "target_audience": row[4],
            "expertise": row[5],
            "personal_touch": row[6],
            "market_scope": row[7],
            "primary_market": row[8],
            "currency": row[9],
            "locale_notes": row[10],
            "tone": row[11],
            "goal": row[12],
        }

        audience_analysis = {
            "id": row[13],
            "audience_profile": row[14],
            "pains": row[15],
            "desires": row[16],
            "objections": row[17],
            "trigger_moments": row[18],
            "proof_points": row[19],
            "audience_language": row[20],
            "market_context": row[21],
            "content_angles": row[22],
            "positioning": row[23],
            "known_for": row[24],
        }

        return profile, audience_analysis


def save_content_ideas(
    conn,
    user_profile_id: str,
    audience_analysis_id: str,
    ideas: list
) -> list:
    idea_ids = []

    with conn.cursor() as cur:
        for idea in ideas:
            idea_id = str(uuid.uuid4())
            idea_ids.append(idea_id)

            cur.execute("""
                INSERT INTO content_ideas (
                    id,
                    user_profile_id,
                    audience_analysis_id,
                    title,
                    hook,
                    angle,
                    topic,
                    post_format
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                idea_id,
                user_profile_id,
                audience_analysis_id,
                idea["title"],
                idea["hook"],
                idea["angle"],
                idea["topic"],
                idea.get("post_format") or idea.get("content_style") or "how_to",
            ))

    return idea_ids
