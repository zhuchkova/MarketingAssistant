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
                up.personal_touch,
                up.tone,
                up.goal,
                aa.audience_profile,
                aa.pains,
                aa.desires,
                aa.objections,
                aa.trigger_moments,
                aa.proof_points,
                aa.audience_language,
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
            "personal_touch": row[5],
            "tone": row[6],
            "goal": row[7],
            "audience_profile": row[8],
            "pains": row[9],
            "desires": row[10],
            "objections": row[11],
            "trigger_moments": row[12],
            "proof_points": row[13],
            "audience_language": row[14],
            "positioning": row[15],
            "known_for": row[16],
            "post_id": row[17],
            "hook": row[18],
            "body": row[19],
            "cta": row[20],
            "final_text": row[21],
            "platform": row[22],
            "post_goal": row[23],
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
