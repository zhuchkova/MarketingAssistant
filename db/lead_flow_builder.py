def default_opening_dm(lead_magnet: dict) -> str:
    title = (lead_magnet.get("title") or "this").strip()
    description = (lead_magnet.get("description") or "").strip()

    if title and description:
        return (
            "Hey there! Thanks so much for your interest.\n\n"
            f"Click below and I’ll send {title} in just a sec."
        )

    if title and title != "this":
        return (
            "Hey there! Thanks so much for your interest.\n\n"
            f"Click below and I’ll send {title} in just a sec."
        )

    return (
        "Hey there! Thanks so much for your interest.\n\n"
        "Click below and I’ll send it in just a sec."
    )


def build_manychat_setup(lead_magnet: dict) -> dict:
    trigger_type = lead_magnet.get("trigger_type") or "specific_word"
    trigger_keyword = lead_magnet.get("suggested_keyword") or "INFO"
    public_reply = lead_magnet.get("public_comment_reply") or "Sent it to you. Check your DMs."
    opening_button = lead_magnet.get("opening_dm_button_label") or "Send me the link"
    link_button = lead_magnet.get("link_button_label") or "Open"
    url = lead_magnet.get("url") or ""
    first_message = lead_magnet.get("delivery_message") or default_opening_dm(lead_magnet)
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
        f"Add this opening DM text: {first_message}",
        f"Set the opening DM button label to: {opening_button}",
    ])
    if url:
        setup_steps.append(f"After the button click, add a link step with URL {url} and button label: {link_button}")
    else:
        setup_steps.append("After the button click, add the next-step message or details. No URL is required for this flow.")
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
        "opening_dm_text": first_message,
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
    return {
        "trigger_keyword": setup["trigger_keyword"],
        "public_comment_reply": setup["public_comment_reply"],
        "public_comment_reply_options": setup["public_comment_reply_options"],
        "first_message": lead_magnet.get("delivery_message") or default_opening_dm(lead_magnet),
        "opening_dm_button_label": setup["opening_dm_button_label"],
        "link_button_label": setup["link_button_label"],
        "qualification_question": lead_magnet.get("qualification_question") or "",
        "follow_up": lead_magnet.get("follow_up_cta") or "",
        "manychat_setup": setup,
    }
