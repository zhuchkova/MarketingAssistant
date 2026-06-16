import uuid

def get_profile_with_audience_analysis(conn, profile_id: str) -> tuple[dict, dict]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                up.id,
                up.user_id,
                up.niche,
                up.offer,
                up.target_audience,
                up.expertise,
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
            "tone": row[6],
            "goal": row[7],
        }

        audience_analysis = {
            "id": row[8],
            "audience_profile": row[9],
            "pains": row[10],
            "desires": row[11],
            "objections": row[12],
            "trigger_moments": row[13],
            "proof_points": row[14],
            "audience_language": row[15],
            "content_angles": row[16],
            "positioning": row[17],
            "known_for": row[18],
        }

        return profile, audience_analysis


def save_content_ideas(
    conn,
    user_profile_id: str,
    audience_analysis_id: str,
    ideas: list[dict]
) -> list[str]:
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
                    topic
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                idea_id,
                user_profile_id,
                audience_analysis_id,
                idea["title"],
                idea["hook"],
                idea["angle"],
                idea["topic"],
            ))

    return idea_ids
