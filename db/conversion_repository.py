EMPTY_LEAD_MAGNET_CONTEXT = {
    "lead_magnet_id": None,
    "lead_magnet_title": None,
    "lead_magnet_url": None,
    "lead_magnet_description": None,
    "lead_magnet_keyword": None,
    "lead_magnet_trigger_type": None,
    "lead_magnet_public_comment_reply": None,
    "lead_magnet_delivery_message": None,
    "lead_magnet_second_dm_message": None,
    "lead_magnet_opening_dm_button_label": None,
    "lead_magnet_link_button_label": None,
    "lead_magnet_qualification_question": None,
    "lead_magnet_follow_up_cta": None,
    "lead_magnet_preferred_post_goal": None,
    "lead_magnet_manychat_setup": {},
}


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
                aa.positioning,
                aa.known_for,
                p.id AS post_id,
                p.hook,
                p.body,
                p.cta,
                p.final_text,
                p.lead_magnet_id,
                p.instagram_content_type,
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
            "positioning": row[20],
            "known_for": row[21],
            "post_id": row[22],
            "hook": row[23],
            "body": row[24],
            "cta": row[25],
            "final_text": row[26],
            "post_lead_magnet_id": row[27],
            "instagram_content_type": row[28],
            "platform": row[29],
            "post_goal": row[30],
            **EMPTY_LEAD_MAGNET_CONTEXT,
        }


def attach_lead_magnet_context(context: dict, lead_magnet: dict = None) -> dict:
    context = {**context, **EMPTY_LEAD_MAGNET_CONTEXT}

    if lead_magnet:
        context.update({
            "lead_magnet_id": lead_magnet.get("id"),
            "lead_magnet_title": lead_magnet.get("title"),
            "lead_magnet_url": lead_magnet.get("url"),
            "lead_magnet_description": lead_magnet.get("description"),
            "lead_magnet_keyword": lead_magnet.get("suggested_keyword"),
            "lead_magnet_trigger_type": lead_magnet.get("trigger_type"),
            "lead_magnet_public_comment_reply": lead_magnet.get("public_comment_reply"),
            "lead_magnet_delivery_message": lead_magnet.get("delivery_message"),
            "lead_magnet_second_dm_message": lead_magnet.get("second_dm_message"),
            "lead_magnet_opening_dm_button_label": lead_magnet.get("opening_dm_button_label"),
            "lead_magnet_link_button_label": lead_magnet.get("link_button_label"),
            "lead_magnet_qualification_question": lead_magnet.get("qualification_question"),
            "lead_magnet_follow_up_cta": lead_magnet.get("follow_up_cta"),
            "lead_magnet_preferred_post_goal": lead_magnet.get("preferred_post_goal"),
            "lead_magnet_manychat_setup": lead_magnet.get("manychat_setup") or {},
        })
        return context

    return context
