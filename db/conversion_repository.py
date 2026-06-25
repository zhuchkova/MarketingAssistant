import uuid
from psycopg.types.json import Jsonb


EMPTY_LEAD_MAGNET_CONTEXT = {
    "lead_magnet_id": None,
    "lead_magnet_title": None,
    "lead_magnet_url": None,
    "lead_magnet_description": None,
    "lead_magnet_keyword": None,
    "lead_magnet_trigger_type": None,
    "lead_magnet_public_comment_reply": None,
    "lead_magnet_delivery_message": None,
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


def attach_lead_magnet_context(context: dict, lead_magnet: dict = None, custom_offer: dict = None) -> dict:
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
            "lead_magnet_opening_dm_button_label": lead_magnet.get("opening_dm_button_label"),
            "lead_magnet_link_button_label": lead_magnet.get("link_button_label"),
            "lead_magnet_qualification_question": lead_magnet.get("qualification_question"),
            "lead_magnet_follow_up_cta": lead_magnet.get("follow_up_cta"),
            "lead_magnet_preferred_post_goal": lead_magnet.get("preferred_post_goal"),
            "lead_magnet_manychat_setup": lead_magnet.get("manychat_setup") or {},
        })
        return context

    if custom_offer:
        context.update({
            "lead_magnet_title": custom_offer.get("custom_offer_title"),
            "lead_magnet_url": custom_offer.get("custom_offer_url"),
            "lead_magnet_description": custom_offer.get("custom_offer_description"),
            "lead_magnet_trigger_type": custom_offer.get("custom_trigger_type"),
            "lead_magnet_keyword": custom_offer.get("custom_keyword"),
            "lead_magnet_public_comment_reply": custom_offer.get("custom_public_comment_reply"),
            "lead_magnet_delivery_message": custom_offer.get("custom_first_message"),
            "lead_magnet_opening_dm_button_label": custom_offer.get("custom_opening_dm_button_label"),
            "lead_magnet_link_button_label": custom_offer.get("custom_link_button_label"),
            "lead_magnet_qualification_question": custom_offer.get("custom_qualification_question"),
            "lead_magnet_follow_up_cta": custom_offer.get("custom_follow_up"),
        })

    return context


def save_manychat_flow(conn, post_id: str, flow: dict, lead_magnet_id: str = None) -> str:
    flow_id = str(uuid.uuid4())

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO manychat_flows (
                id,
                post_id,
                lead_magnet_id,
                trigger_keyword,
                public_comment_reply,
                first_message,
                qualification_question,
                follow_up,
                manychat_setup
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            flow_id,
            post_id,
            lead_magnet_id,
            flow["trigger_keyword"],
            flow.get("public_comment_reply"),
            flow["first_message"],
            flow["qualification_question"],
            flow["follow_up"],
            Jsonb(flow.get("manychat_setup") or {}),
        ))

    return flow_id


def build_manychat_setup(lead_magnet: dict) -> dict:
    trigger_type = lead_magnet.get("trigger_type") or "specific_word"
    trigger_keyword = lead_magnet.get("suggested_keyword") or "INFO"
    public_reply = lead_magnet.get("public_comment_reply") or "Sent it to you. Check your DMs."
    opening_button = lead_magnet.get("opening_dm_button_label") or "Send me the link"
    link_button = lead_magnet.get("link_button_label") or "Open"
    url = lead_magnet.get("url") or ""
    first_message = lead_magnet.get("delivery_message") or ""
    qualification_question = lead_magnet.get("qualification_question") or ""
    follow_up = lead_magnet.get("follow_up_cta") or ""

    setup_steps = [
        "Create an Instagram Comments automation in ManyChat.",
        f"Set the comment trigger to {'any word or reaction' if trigger_type == 'any_word' else 'a specific word or reaction'}.",
    ]
    if trigger_type != "any_word":
        setup_steps.append(f"Use the trigger keyword '{trigger_keyword}'.")
    setup_steps.extend([
        f"Turn on public comment reply and use: {public_reply}",
        f"Add an opening DM with button label: {opening_button}",
    ])
    if first_message:
        setup_steps.append(f"Use this opening DM text: {first_message}")
    if url:
        setup_steps.append(f"Add a link step with URL {url} and button label: {link_button}")
    else:
        setup_steps.append("Add the next-step message or details. No URL is required for this flow.")
    if qualification_question:
        setup_steps.append(f"Optionally ask this qualification question: {qualification_question}")
    if follow_up:
        setup_steps.append(f"Optionally add this follow-up: {follow_up}")
    setup_steps.extend([
        "Preview the Comments and DM tabs before going live.",
        "Click Go Live in ManyChat when ready.",
    ])

    return {
        "manual_required": True,
        "comment_trigger_mode": trigger_type,
        "public_comment_reply": public_reply,
        "public_comment_reply_options": [
            public_reply,
            "Just sent it your way.",
            "Thanks for commenting. Check your DMs.",
        ],
        "trigger_keyword": trigger_keyword,
        "opening_dm_button_label": opening_button,
        "link_button_label": link_button,
        "flow_type": "instagram_comment_to_dm",
        "lead_magnet_used": bool(url),
        "lead_magnet_url": url,
        "setup_steps": setup_steps,
        "api_supported_parts": [
            "Account metadata",
            "Tags and custom fields",
            "Sending content or flows to existing contacts",
        ],
    }


def flow_from_lead_magnet(lead_magnet: dict) -> dict:
    setup = build_manychat_setup(lead_magnet)
    first_message = lead_magnet.get("delivery_message") or default_opening_dm(lead_magnet)
    return {
        "trigger_keyword": setup["trigger_keyword"],
        "public_comment_reply": setup["public_comment_reply"],
        "public_comment_reply_options": setup["public_comment_reply_options"],
        "first_message": first_message,
        "opening_dm_button_label": setup["opening_dm_button_label"],
        "link_button_label": setup["link_button_label"],
        "qualification_question": lead_magnet.get("qualification_question") or "",
        "follow_up": lead_magnet.get("follow_up_cta") or "",
        "manychat_setup": setup,
    }


def default_opening_dm(lead_magnet: dict) -> str:
    return (
        "Hey there! I’m so happy you’re here, thanks so much for your interest.\n\n"
        "Click below and I’ll send it in just a sec."
    )
