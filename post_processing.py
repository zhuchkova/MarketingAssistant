import re
from typing import Optional


COMMENT_WORD_RE = re.compile(r"\bcomments?\b|\bcommenting\b", re.IGNORECASE)
REEL_CAPTION_HEADING_RE = re.compile(
    r"^\s*(?:instagram\s+|reel\s+)?caption(?:\s*:\s*(.*)|\s*)$",
    re.IGNORECASE,
)
REEL_NON_CAPTION_HEADING_RE = re.compile(
    r"^\s*(?:"
    r"reel\s+script|script|spoken\s+script|voice\s*over|voiceover|"
    r"on[-\s]*screen\s+text|overlay\s+text|text\s+overlay|"
    r"shot\s+list|shots?|scene|scenes?|b[-\s]*roll|visuals?"
    r")(?:\s*:.*|\s*)$",
    re.IGNORECASE,
)


def enforce_automation_cta(generated_post: dict, automation_resource: Optional[dict]) -> dict:
    if not automation_resource:
        return generated_post

    keyword = str(automation_resource.get("suggested_keyword") or "").strip()
    if not keyword:
        return generated_post

    changed = False
    cta = str(generated_post.get("cta") or "").strip()
    keyword_upper = keyword.upper()
    if not is_comment_keyword_cta(cta, keyword):
        title = str(automation_resource.get("title") or "the resource").strip()
        generated_post["cta"] = f"Comment {keyword_upper} and I'll send you {title}."
        changed = True

    body = str(generated_post.get("body") or "")
    cleaned_body = remove_duplicate_comment_keyword_ctas(body, keyword)
    if cleaned_body != body:
        generated_post["body"] = cleaned_body
        changed = True

    if changed:
        generated_post["final_text"] = ""

    return generated_post


def remove_duplicate_comment_keyword_ctas(body: str, keyword: str) -> str:
    keyword = str(keyword or "").strip()
    if not body or not keyword:
        return body

    paragraphs = re.split(r"(\n\s*\n)", body)
    cleaned = []

    for part in paragraphs:
        if not part.strip():
            cleaned.append(part)
            continue

        cleaned_part = remove_comment_keyword_sentences(part, keyword)
        if cleaned_part.strip():
            cleaned.append(cleaned_part)

    return "".join(cleaned).strip()


def remove_comment_keyword_sentences(text: str, keyword: str) -> str:
    pieces = re.split(r"([^.!?\n]+[.!?]?)", text)
    cleaned = []

    for piece in pieces:
        if not piece:
            continue
        if is_comment_keyword_cta(piece, keyword):
            continue
        cleaned.append(piece)

    return "".join(cleaned).strip()


def is_comment_keyword_cta(text: str, keyword: str) -> bool:
    return bool(COMMENT_WORD_RE.search(text) and keyword_in_text(text, keyword))


def keyword_in_text(text: str, keyword: str) -> bool:
    normalized_text = re.sub(r"[^a-z0-9]+", "", text.lower())
    normalized_keyword = re.sub(r"[^a-z0-9]+", "", keyword.lower())
    return bool(normalized_keyword and normalized_keyword in normalized_text)


def enforce_reel_caption_only(generated_post: dict, instagram_content_type: Optional[str]) -> dict:
    if instagram_content_type != "reel":
        return generated_post

    body = str(generated_post.get("body") or "")
    caption = extract_reel_caption(body)
    if not caption or caption == body.strip():
        return generated_post

    generated_post["body"] = caption
    generated_post["final_text"] = ""
    return generated_post


def extract_reel_caption(body: str) -> str:
    body = str(body or "").strip()
    if not body:
        return body

    caption = extract_labeled_caption(body)
    if caption:
        return caption

    if not has_reel_script_markers(body):
        return body

    paragraphs = re.split(r"\n\s*\n", body)
    cleaned = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip() and not is_reel_script_paragraph(paragraph)
    ]
    return "\n\n".join(cleaned).strip()


def extract_labeled_caption(body: str) -> str:
    lines = body.splitlines()
    caption_lines = []
    collecting = False

    for line in lines:
        caption_match = REEL_CAPTION_HEADING_RE.match(line)
        if caption_match:
            collecting = True
            inline_caption = (caption_match.group(1) or "").strip()
            if inline_caption:
                caption_lines.append(inline_caption)
            continue

        if collecting and REEL_NON_CAPTION_HEADING_RE.match(line):
            break

        if collecting:
            caption_lines.append(line)

    return "\n".join(caption_lines).strip()


def has_reel_script_markers(body: str) -> bool:
    return any(REEL_NON_CAPTION_HEADING_RE.match(line) for line in body.splitlines())


def is_reel_script_paragraph(paragraph: str) -> bool:
    lines = paragraph.splitlines()
    return any(REEL_NON_CAPTION_HEADING_RE.match(line) for line in lines)
