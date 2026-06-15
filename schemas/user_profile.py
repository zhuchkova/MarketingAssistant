from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


def clean_required_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("This field is required")
    return value


def validate_uuid(value: str | None) -> str | None:
    if value is None:
        return None
    try:
        return str(UUID(str(value)))
    except ValueError:
        raise ValueError("ID must be a valid UUID")


class CreateUserProfileRequest(BaseModel):
    id: str | None = None
    profile_name: str
    niche: str
    offer: str
    target_audience: str
    expertise: str
    tone: str
    goal: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str | None) -> str | None:
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "22222222-2222-2222-2222-222222222444",
                "profile_name": "AI automation 1",
                "niche": "AI automation for founders",
                "offer": "AI marketing workflows and systems",
                "target_audience": "early-stage founders struggling with marketing",
                "expertise": "ML engineer building AI agents",
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "profile_name": "AI automation 1",
                "niche": "AI automation for founders",
                "offer": "AI marketing workflows and systems",
                "target_audience": "early-stage founders struggling with marketing",
                "expertise": "ML engineer building AI agents",
                "tone": "bold, practical",
                "goal": "generate leads"
            }
        }
    )
