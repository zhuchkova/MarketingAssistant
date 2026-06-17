from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


ALLOWED_POST_FORMATS = {
    "personal_story",
    "mistakes",
    "day_in_life",
    "contrarian",
    "how_to",
    "checklist",
    "myth_busting",
    "client_example",
    "behind_scenes",
    "objection_handling",
}

FORMAT_LABELS = {
    "personal_story": "personal story",
    "mistakes": "mistakes",
    "day_in_life": "day in life",
    "contrarian": "contrarian",
    "how_to": "how-to",
    "checklist": "checklist",
    "myth_busting": "myth busting",
    "client_example": "client example",
    "behind_scenes": "behind the scenes",
    "objection_handling": "objection handling",
}

PostFormat = Literal[
    "personal_story",
    "mistakes",
    "day_in_life",
    "contrarian",
    "how_to",
    "checklist",
    "myth_busting",
    "client_example",
    "behind_scenes",
    "objection_handling",
]


def clean_required_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("This field is required")
    return value


def capitalize_first(value: str) -> str:
    value = value.strip()
    return value[:1].upper() + value[1:] if value else value


def validate_uuid(value: str) -> str:
    try:
        return str(UUID(str(value)))
    except ValueError:
        raise ValueError("ID must be a valid UUID")


def validate_post_format(value: str) -> str:
    value = value.strip().lower()
    if value not in ALLOWED_POST_FORMATS:
        raise ValueError(f"post_format must be one of: {', '.join(sorted(ALLOWED_POST_FORMATS))}")
    return value


class ContentIdeaRequest(BaseModel):
    title: str
    hook: str
    angle: str
    topic: str
    post_format: PostFormat

    @field_validator("title", "hook", "angle", "topic")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        return capitalize_first(clean_required_text(value))

    @field_validator("post_format")
    @classmethod
    def clean_post_format(cls, value: str) -> str:
        return validate_post_format(value)

    @model_validator(mode="after")
    def validate_angle_is_framing(self):
        angle = self.angle.strip().lower().replace("_", " ").replace("-", " ")
        post_format = self.post_format
        format_label = FORMAT_LABELS[post_format]
        if angle in {post_format.replace("_", " "), format_label}:
            raise ValueError("Idea framing must be more specific than the post format")
        return self

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The mistake that made my content sound generic",
                "hook": "I used to write posts that sounded smart but got ignored.",
                "angle": "A personal lesson about making content more specific",
                "topic": "content positioning",
                "post_format": "personal_story",
            }
        }
    )


class GenerateIdeasRequest(BaseModel):
    count: int = 10

    @field_validator("count")
    @classmethod
    def validate_count(cls, value: int) -> int:
        if value < 1 or value > 30:
            raise ValueError("count must be between 1 and 30")
        return value
