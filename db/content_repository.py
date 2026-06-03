import uuid

def get_content_generation_context(conn, content_idea_id: str) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                up.id,
                up.niche,
                up.offer,
                up.target_audience,
                up.expertise,
                up.tone,
                up.goal,
                aa.audience_profile,
                aa.pains,
                aa.desires,
                aa.objections,
                aa.content_angles,
                aa.positioning,
                aa.known_for,
                ci.id,
                ci.title,
                ci.hook,
                ci.angle,
                ci.topic
            FROM content_ideas ci
            JOIN user_profiles up
                ON ci.user_profile_id = up.id
            JOIN audience_analyses aa
                ON ci.audience_analysis_id = aa.id
            WHERE ci.id = %s
        """, (content_idea_id,))

        row = cur.fetchone()

        if not row:
            raise ValueError("Content idea not found")

        return {
            "user_profile_id": row[0],
            "niche": row[1],
            "offer": row[2],
            "target_audience": row[3],
            "expertise": row[4],
            "tone": row[5],
            "goal": row[6],
            "audience_profile": row[7],
            "pains": row[8],
            "desires": row[9],
            "objections": row[10],
            "content_angles": row[11],
            "positioning": row[12],
            "known_for": row[13],
            "content_idea_id": row[14],
            "idea_title": row[15],
            "idea_hook": row[16],
            "idea_angle": row[17],
            "idea_topic": row[18],
        }


def get_lookup_id(conn, table_name: str, name: str) -> int:
    allowed_tables = {
        "platforms",
        "post_formats",
        "post_goals",
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid lookup table")

    with conn.cursor() as cur:
        cur.execute(
            f"SELECT id FROM {table_name} WHERE name = %s",
            (name,)
        )
        row = cur.fetchone()

        if not row:
            raise ValueError(f"{name} not found in {table_name}")

        return row[0]


def save_post(conn, data: dict) -> str:
    post_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO posts (
                id,
                user_profile_id,
                content_idea_id,
                platform_id,
                post_format_id,
                post_goal_id,
                hook,
                body,
                cta,
                final_text
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            post_id,
            data["user_profile_id"],
            data["content_idea_id"],
            data["platform_id"],
            data["post_format_id"],
            data["post_goal_id"],
            data["hook"],
            data["body"],
            data["cta"],
            data["final_text"],
        ))

    return post_id