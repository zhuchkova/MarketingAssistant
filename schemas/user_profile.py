from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


def clean_required_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("This field is required")
    return value


def validate_uuid(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    try:
        return str(UUID(str(value)))
    except ValueError:
        raise ValueError("ID must be a valid UUID")


class CreateUserProfileRequest(BaseModel):
    id: Optional[str] = None
    profile_name: str
    niche: str
    offer: str
    target_audience: str
    expertise: str
    personal_touch: Optional[str] = None
    market_scope: Optional[str] = None
    primary_market: Optional[str] = None
    currency: Optional[str] = None
    locale_notes: Optional[str] = None
    tone: str
    goal: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: Optional[str]) -> Optional[str]:
        return validate_uuid(value)

    @field_validator(
        "profile_name",
        "niche",
        "offer",
        "target_audience",
        "expertise",
        "tone",
        "goal",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        return clean_required_text(value)

    @field_validator("personal_touch", "market_scope", "primary_market", "currency", "locale_notes")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "22222222-2222-2222-2222-222222222444",
                "profile_name": "AI automation 1",
                "niche": "AI automation for founders",
                "offer": "AI marketing workflows and systems",
                "target_audience": "early-stage founders struggling with marketing",
                "expertise": "ML engineer building AI agents",
                "personal_touch": "I used to build these workflows manually before automating them.",
                "market_scope": "local",
                "primary_market": "Berlin, Germany",
                "currency": "EUR",
                "locale_notes": "Use local European cafe examples but write in English.",
                "tone": "bold, practical",
                "goal": "generate leads"
            }
        }
    )


class UpdateUserProfileRequest(BaseModel):
    profile_name: str
    niche: str
    offer: str
    target_audience: str
    expertise: str
    personal_touch: Optional[str] = None
    market_scope: Optional[str] = None
    primary_market: Optional[str] = None
    currency: Optional[str] = None
    locale_notes: Optional[str] = None
    tone: str
    goal: str

    @field_validator(
        "profile_name",
        "niche",
        "offer",
        "target_audience",
        "expertise",
        "tone",
        "goal",
    )
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        return clean_required_text(value)

    @field_validator("personal_touch", "market_scope", "primary_market", "currency", "locale_notes")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "profile_name": "AI automation 1",
                "niche": "AI automation for founders",
                "offer": "AI marketing workflows and systems",
                "target_audience": "early-stage founders struggling with marketing",
                "expertise": "ML engineer building AI agents",
                "personal_touch": "I used to build these workflows manually before automating them.",
                "market_scope": "local",
                "primary_market": "Berlin, Germany",
                "currency": "EUR",
                "locale_notes": "Use local European cafe examples but write in English.",
                "tone": "bold, practical",
                "goal": "generate leads"
            }
        }
    )
