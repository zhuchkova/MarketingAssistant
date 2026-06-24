from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from schemas.post_generation import ALLOWED_POST_GOALS


def clean_optional_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = value.strip()
    return value or None


class LeadMagnetRequest(BaseModel):
    title: str
    url: Optional[str] = None
    description: Optional[str] = None
    suggested_keyword: Optional[str] = None
    public_comment_reply: Optional[str] = None
    delivery_message: Optional[str] = None
    follow_up_cta: Optional[str] = None
    preferred_post_goal: Optional[str] = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title is required")
        return value

    @field_validator(
        "url",
        "description",
        "suggested_keyword",
        "public_comment_reply",
        "delivery_message",
        "follow_up_cta",
        "preferred_post_goal",
    )
    @classmethod
    def clean_optional_fields(cls, value: Optional[str]) -> Optional[str]:
        return clean_optional_text(value)

    @field_validator("preferred_post_goal")
    @classmethod
    def validate_preferred_post_goal(cls, value: Optional[str]) -> Optional[str]:
        value = clean_optional_text(value)
        if value is None:
            return None
        value = value.lower()
        if value not in ALLOWED_POST_GOALS:
            raise ValueError(
                "preferred_post_goal must be one of: "
                f"{', '.join(sorted(ALLOWED_POST_GOALS))}"
            )
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Free content planning guide",
                "url": "https://example.com/guide",
                "description": "A short guide for planning a week of posts.",
                "suggested_keyword": "GUIDE",
                "public_comment_reply": "Sent it to you now.",
                "delivery_message": "Here is the guide I mentioned.",
                "follow_up_cta": "If you want help applying it, book a session here.",
                "preferred_post_goal": "download"
            }
        }
    )
