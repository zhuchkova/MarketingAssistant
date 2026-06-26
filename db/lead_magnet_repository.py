import uuid
from psycopg.types.json import Jsonb

from db.lead_flow_builder import build_manychat_setup


def _has_flow_details(data: dict) -> bool:
    return any(data.get(key) for key in (
        "suggested_keyword",
        "public_comment_reply",
        "public_comment_reply_options",
        "delivery_message",
        "second_dm_message",
        "opening_dm_button_label",
        "link_button_label",
        "qualification_question",
        "follow_up_cta",
    ))


def list_lead_magnets(conn, profile_id: str) -> list:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                id,
                title,
                url,
                description,
                suggested_keyword,
                trigger_type,
                public_comment_reply,
                delivery_message,
                second_dm_message,
                opening_dm_button_label,
                link_button_label,
                qualification_question,
                follow_up_cta,
                preferred_post_goal,
                manychat_setup,
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
            "trigger_type": row[5],
            "public_comment_reply": row[6],
            "delivery_message": row[7],
            "second_dm_message": row[8],
            "opening_dm_button_label": row[9],
            "link_button_label": row[10],
            "qualification_question": row[11],
            "follow_up_cta": row[12],
            "preferred_post_goal": row[13],
            "manychat_setup": row[14] or {},
            "is_primary": row[15],
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
                trigger_type,
                public_comment_reply,
                delivery_message,
                second_dm_message,
                opening_dm_button_label,
                link_button_label,
                qualification_question,
                follow_up_cta,
                preferred_post_goal,
                manychat_setup,
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
        "trigger_type": row[5],
        "public_comment_reply": row[6],
        "delivery_message": row[7],
        "second_dm_message": row[8],
        "opening_dm_button_label": row[9],
        "link_button_label": row[10],
        "qualification_question": row[11],
        "follow_up_cta": row[12],
        "preferred_post_goal": row[13],
        "manychat_setup": row[14] or {},
        "is_primary": row[15],
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
                trigger_type,
                public_comment_reply,
                delivery_message,
                second_dm_message,
                opening_dm_button_label,
                link_button_label,
                qualification_question,
                follow_up_cta,
                preferred_post_goal,
                manychat_setup,
                is_primary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lead_magnet_id,
            profile_id,
            data["title"],
            data.get("url"),
            data.get("description"),
            data.get("suggested_keyword"),
            data.get("trigger_type") or "specific_word",
            data.get("public_comment_reply"),
            data.get("delivery_message"),
            data.get("second_dm_message"),
            data.get("opening_dm_button_label"),
            data.get("link_button_label"),
            data.get("qualification_question"),
            data.get("follow_up_cta"),
            data.get("preferred_post_goal"),
            Jsonb(build_manychat_setup(data) if _has_flow_details(data) else {}),
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
                trigger_type = %s,
                public_comment_reply = %s,
                delivery_message = %s,
                second_dm_message = %s,
                opening_dm_button_label = %s,
                link_button_label = %s,
                qualification_question = %s,
                follow_up_cta = %s,
                preferred_post_goal = %s,
                manychat_setup = %s
            WHERE id = %s AND user_profile_id = %s
        """, (
            data["title"],
            data.get("url"),
            data.get("description"),
            data.get("suggested_keyword"),
            data.get("trigger_type") or "specific_word",
            data.get("public_comment_reply"),
            data.get("delivery_message"),
            data.get("second_dm_message"),
            data.get("opening_dm_button_label"),
            data.get("link_button_label"),
            data.get("qualification_question"),
            data.get("follow_up_cta"),
            data.get("preferred_post_goal"),
            Jsonb(build_manychat_setup(data) if _has_flow_details(data) else {}),
            lead_magnet_id,
            profile_id,
        ))

        if cur.rowcount == 0:
            raise ValueError("Lead magnet not found")


def update_lead_magnet_flow(conn, lead_magnet_id: str, profile_id: str, flow: dict) -> None:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT title, url, description, preferred_post_goal
            FROM lead_magnets
            WHERE id = %s AND user_profile_id = %s
        """, (lead_magnet_id, profile_id))
        existing = cur.fetchone()

    if not existing:
        raise ValueError("Lead magnet not found")

    final_data = {
        "title": existing[0],
        "url": existing[1],
        "description": existing[2],
        "preferred_post_goal": existing[3],
        "suggested_keyword": flow.get("trigger_keyword"),
        "trigger_type": (flow.get("manychat_setup") or {}).get("comment_trigger_mode") or "specific_word",
        "public_comment_reply": flow.get("public_comment_reply"),
        "public_comment_reply_options": flow.get("public_comment_reply_options"),
        "delivery_message": flow.get("first_message"),
        "second_dm_message": flow.get("second_message"),
        "opening_dm_button_label": flow.get("opening_dm_button_label"),
        "link_button_label": flow.get("link_button_label"),
        "qualification_question": flow.get("qualification_question"),
        "follow_up_cta": flow.get("follow_up"),
    }
    setup = build_manychat_setup(final_data)

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE lead_magnets
            SET suggested_keyword = %s,
                trigger_type = %s,
                public_comment_reply = %s,
                delivery_message = %s,
                second_dm_message = %s,
                opening_dm_button_label = %s,
                link_button_label = %s,
                qualification_question = %s,
                follow_up_cta = %s,
                manychat_setup = %s
            WHERE id = %s AND user_profile_id = %s
        """, (
            final_data["suggested_keyword"],
            final_data["trigger_type"],
            final_data["public_comment_reply"],
            final_data["delivery_message"],
            final_data["second_dm_message"],
            final_data["opening_dm_button_label"],
            final_data["link_button_label"],
            final_data["qualification_question"],
            final_data["follow_up_cta"],
            Jsonb(setup),
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
