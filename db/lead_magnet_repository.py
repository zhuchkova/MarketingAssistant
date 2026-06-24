import uuid


def list_lead_magnets(conn, profile_id: str) -> list:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                title,
                url,
                description,
                suggested_keyword,
                public_comment_reply,
                delivery_message,
                follow_up_cta,
                preferred_post_goal,
                is_primary
            FROM lead_magnets
            WHERE user_profile_id = %s
            ORDER BY is_primary DESC, title
        """, (profile_id,))
        rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "description": row[3],
            "suggested_keyword": row[4],
            "public_comment_reply": row[5],
            "delivery_message": row[6],
            "follow_up_cta": row[7],
            "preferred_post_goal": row[8],
            "is_primary": row[9],
        }
        for row in rows
    ]


def get_lead_magnet(conn, lead_magnet_id: str, profile_id: str) -> dict:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                title,
                url,
                description,
                suggested_keyword,
                public_comment_reply,
                delivery_message,
                follow_up_cta,
                preferred_post_goal,
                is_primary
            FROM lead_magnets
            WHERE id = %s AND user_profile_id = %s
        """, (lead_magnet_id, profile_id))
        row = cur.fetchone()

    if not row:
        raise ValueError("Lead magnet not found")

    return {
        "id": row[0],
        "title": row[1],
        "url": row[2],
        "description": row[3],
        "suggested_keyword": row[4],
        "public_comment_reply": row[5],
        "delivery_message": row[6],
        "follow_up_cta": row[7],
        "preferred_post_goal": row[8],
        "is_primary": row[9],
    }


def save_lead_magnet(conn, profile_id: str, data: dict, is_primary: bool = False) -> str:
    lead_magnet_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        if is_primary:
            cur.execute(
                "UPDATE lead_magnets SET is_primary = FALSE WHERE user_profile_id = %s",
                (profile_id,),
            )

        cur.execute("""
            INSERT INTO lead_magnets (
                id,
                user_profile_id,
                title,
                url,
                description,
                suggested_keyword,
                public_comment_reply,
                delivery_message,
                follow_up_cta,
                preferred_post_goal,
                is_primary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lead_magnet_id,
            profile_id,
            data["title"],
            data.get("url"),
            data.get("description"),
            data.get("suggested_keyword"),
            data.get("public_comment_reply"),
            data.get("delivery_message"),
            data.get("follow_up_cta"),
            data.get("preferred_post_goal"),
            is_primary,
        ))

    return lead_magnet_id


def update_lead_magnet(conn, lead_magnet_id: str, profile_id: str, data: dict) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lead_magnets
            SET title = %s,
                url = %s,
                description = %s,
                suggested_keyword = %s,
                public_comment_reply = %s,
                delivery_message = %s,
                follow_up_cta = %s,
                preferred_post_goal = %s
            WHERE id = %s AND user_profile_id = %s
        """, (
            data["title"],
            data.get("url"),
            data.get("description"),
            data.get("suggested_keyword"),
            data.get("public_comment_reply"),
            data.get("delivery_message"),
            data.get("follow_up_cta"),
            data.get("preferred_post_goal"),
            lead_magnet_id,
            profile_id,
        ))

        if cur.rowcount == 0:
            raise ValueError("Lead magnet not found")


def delete_lead_magnet(conn, lead_magnet_id: str, profile_id: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM lead_magnets WHERE id = %s AND user_profile_id = %s",
            (lead_magnet_id, profile_id),
        )
        if cur.rowcount == 0:
            raise ValueError("Lead magnet not found")
