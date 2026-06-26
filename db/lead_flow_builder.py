def default_opening_dm(lead_magnet: dict) -> str:
    title = (lead_magnet.get("title") or "this").strip()
    description = (lead_magnet.get("description") or "").strip()

    if title and description:
        return (
            "Hey there, I’m so happy you’re here. Thanks so much for your interest.\n\n"
            f"Click below and I’ll send {title} in just a sec."
        )

    if title and title != "this":
        return (
            "Hey there, I’m so happy you’re here. Thanks so much for your interest.\n\n"
            f"Click below and I’ll send {title} in just a sec."
        )

    return (
        "Hey there, I’m so happy you’re here. Thanks so much for your interest.\n\n"
        "Click below and I’ll send it in just a sec."
    )


def build_manychat_setup(lead_magnet: dict) -> dict:
    trigger_type = lead_magnet.get("trigger_type") or "specific_word"
    trigger_keyword = lead_magnet.get("suggested_keyword") or ""
    public_reply = lead_magnet.get("public_comment_reply") or ""
    reply_options = lead_magnet.get("public_comment_reply_options") or []
    reply_options = [option for option in reply_options if option]
    if public_reply and public_reply not in reply_options:
        reply_options = [public_reply, *reply_options]
    if public_reply:
        reply_options = (reply_options + [
            "Just sent it your way.",
            "Thanks for commenting. Check your DMs.",
        ])[:3]
    url = lead_magnet.get("url") or ""
    opening_button = lead_magnet.get("opening_dm_button_label") or ""
    link_button = (lead_magnet.get("link_button_label") or "") if url else ""
    first_message = lead_magnet.get("delivery_message") or ""
    second_message = lead_magnet.get("second_dm_message") or ""
    qualification_question = lead_magnet.get("qualification_question") or ""
    follow_up = lead_magnet.get("follow_up_cta") or ""

    setup_steps = [
        "Create an Instagram Comments automation in ManyChat.",
        f"Set the comment trigger to {'any word or reaction' if trigger_type == 'any_word' else 'a specific word or reaction'}.",
    ]
    if trigger_type != "any_word" and trigger_keyword:
        setup_steps.append(f"Use the trigger keyword '{trigger_keyword}'.")
    elif trigger_type != "any_word":
        setup_steps.append("Choose the trigger keyword before going live.")
    if public_reply:
        alternatives = [option for option in reply_options if option != public_reply]
        suffix = f" Alternative replies: {' | '.join(alternatives)}" if alternatives else ""
        setup_steps.append(f"Turn on public comment reply and use: {public_reply}{suffix}")
    else:
        setup_steps.append("Turn on public comment reply and add the reply text.")
    if first_message:
        setup_steps.append(f"Add this opening DM text: {first_message}")
    else:
        setup_steps.append("Add an opening DM text.")
    if opening_button:
        setup_steps.append(f"Set the opening DM button label to: {opening_button}")
    else:
        setup_steps.append("Add an opening DM button label if the flow should continue by button click.")
    if second_message:
        setup_steps.append(f"After the button click, send this second DM text: {second_message}")
    else:
        setup_steps.append("After the button click, add the second DM text or resource details.")
    if url and link_button:
        setup_steps.append(f"Attach URL {url} to the second DM with button label: {link_button}")
    elif url:
        setup_steps.append(f"Attach URL {url} to the second DM.")
    else:
        setup_steps.append("No URL is required for this flow.")
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
        "public_comment_reply_options": reply_options,
        "trigger_keyword": trigger_keyword,
        "opening_dm_text": first_message,
        "second_dm_text": second_message,
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
        "first_message": lead_magnet.get("delivery_message") or setup.get("opening_dm_text") or "",
        "second_message": lead_magnet.get("second_dm_message") or setup.get("second_dm_text") or "",
        "opening_dm_button_label": setup["opening_dm_button_label"],
        "link_button_label": setup["link_button_label"],
        "qualification_question": lead_magnet.get("qualification_question") or "",
        "follow_up": lead_magnet.get("follow_up_cta") or "",
        "manychat_setup": setup,
    }
