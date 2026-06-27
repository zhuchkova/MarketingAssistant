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
                up.personal_touch,
                up.market_scope,
                up.primary_market,
                up.currency,
                up.locale_notes,
                up.tone,
                up.goal,
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
                aa.known_for,
                ci.id,
                ci.title,
                ci.hook,
                ci.angle,
                ci.topic,
                COALESCE(ci.post_format, ci.content_style) AS post_format
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
            "personal_touch": row[5],
            "market_scope": row[6],
            "primary_market": row[7],
            "currency": row[8],
            "locale_notes": row[9],
            "tone": row[10],
            "goal": row[11],
            "audience_profile": row[12],
            "pains": row[13],
            "desires": row[14],
            "objections": row[15],
            "trigger_moments": row[16],
            "proof_points": row[17],
            "audience_language": row[18],
            "market_context": row[19],
            "content_angles": row[20],
            "positioning": row[21],
            "known_for": row[22],
            "content_idea_id": row[23],
            "idea_title": row[24],
            "idea_hook": row[25],
            "idea_angle": row[26],
            "idea_topic": row[27],
            "idea_post_format": row[28],
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
                automation_resource_id,
                instagram_content_type,
                post_length,
                hook,
                body,
                cta,
                final_text
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            post_id,
            data["user_profile_id"],
            data["content_idea_id"],
            data["platform_id"],
            data["post_format_id"],
            data["post_goal_id"],
            data.get("automation_resource_id"),
            data.get("instagram_content_type"),
            data.get("post_length", "medium"),
            data["hook"],
            data["body"],
            data["cta"],
            data["final_text"],
        ))

    return post_id


def update_post_content(conn, post_id: str, data: dict) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE posts
            SET hook = %s,
                body = %s,
                cta = %s,
                final_text = %s
            WHERE id = %s
        """, (
            data["hook"],
            data.get("body", ""),
            data.get("cta", ""),
            data["final_text"],
            post_id,
        ))
