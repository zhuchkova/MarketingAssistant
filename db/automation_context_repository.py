EMPTY_AUTOMATION_RESOURCE_CONTEXT = {
    "automation_resource_id": None,
    "automation_resource_title": None,
    "automation_resource_url": None,
    "automation_resource_description": None,
    "automation_resource_keyword": None,
    "automation_resource_trigger_type": None,
    "automation_resource_public_comment_reply": None,
    "automation_resource_delivery_message": None,
    "automation_resource_second_dm_message": None,
    "automation_resource_opening_dm_button_label": None,
    "automation_resource_link_button_label": None,
    "automation_resource_qualification_question": None,
    "automation_resource_follow_up_cta": None,
    "automation_resource_preferred_post_goal": None,
    "automation_resource_manychat_setup": {},
}


def get_automation_context(conn, post_id: str) -> dict:
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
                p.automation_resource_id,
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
            "post_automation_resource_id": row[27],
            "instagram_content_type": row[28],
            "platform": row[29],
            "post_goal": row[30],
            **EMPTY_AUTOMATION_RESOURCE_CONTEXT,
        }


def attach_automation_resource_context(context: dict, automation_resource: dict = None) -> dict:
    context = {**context, **EMPTY_AUTOMATION_RESOURCE_CONTEXT}

    if automation_resource:
        context.update({
            "automation_resource_id": automation_resource.get("id"),
            "automation_resource_title": automation_resource.get("title"),
            "automation_resource_url": automation_resource.get("url"),
            "automation_resource_description": automation_resource.get("description"),
            "automation_resource_keyword": automation_resource.get("suggested_keyword"),
            "automation_resource_trigger_type": automation_resource.get("trigger_type"),
            "automation_resource_public_comment_reply": automation_resource.get("public_comment_reply"),
            "automation_resource_delivery_message": automation_resource.get("delivery_message"),
            "automation_resource_second_dm_message": automation_resource.get("second_dm_message"),
            "automation_resource_opening_dm_button_label": automation_resource.get("opening_dm_button_label"),
            "automation_resource_link_button_label": automation_resource.get("link_button_label"),
            "automation_resource_qualification_question": automation_resource.get("qualification_question"),
            "automation_resource_follow_up_cta": automation_resource.get("follow_up_cta"),
            "automation_resource_preferred_post_goal": automation_resource.get("preferred_post_goal"),
            "automation_resource_manychat_setup": automation_resource.get("manychat_setup") or {},
        })
        return context

    return context
