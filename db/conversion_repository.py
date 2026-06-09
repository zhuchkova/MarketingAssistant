import uuid


def get_conversion_context(conn, post_id: str) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                up.id AS user_profile_id,
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
                aa.positioning,
                aa.known_for,
                p.id AS post_id,
                p.hook,
                p.body,
                p.cta,
                p.final_text,
                pl.name AS platform,
                pg.name AS post_goal

            FROM posts p
            JOIN user_profiles up
                ON p.user_profile_id = up.id
            JOIN audience_analyses aa
                ON aa.user_profile_id = up.id
            JOIN platforms pl
                ON p.platform_id = pl.id
            LEFT JOIN post_goals pg
                ON p.post_goal_id = pg.id
            WHERE p.id = %s
        """, (post_id,))

        row = cur.fetchone()

        if not row:
            raise ValueError("Post not found")

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
            "positioning": row[11],
            "known_for": row[12],
            "post_id": row[13],
            "hook": row[14],
            "body": row[15],
            "cta": row[16],
            "final_text": row[17],
            "platform": row[18],
            "post_goal": row[19],
        }


def save_manychat_flow(conn, post_id: str, flow: dict) -> str:
    flow_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO manychat_flows (
                id,
                post_id,
                trigger_keyword,
                first_message,
                qualification_question,
                follow_up
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            flow_id,
            post_id,
            flow["trigger_keyword"],
            flow["first_message"],
            flow["qualification_question"],
            flow["follow_up"],
        ))

    return flow_id