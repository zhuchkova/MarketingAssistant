from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


ALLOWED_PLATFORMS = {"instagram", "linkedin"}
ALLOWED_POST_FORMATS = {"story", "how_to", "list", "contrarian"}
ALLOWED_POST_GOALS = {"comment", "dm_keyword", "follow", "download"}


class GeneratePostRequest(BaseModel):
    content_idea_id: str
    platform: str
    post_format: str
    post_goal: str

    @field_validator("content_idea_id")
    @classmethod
    def validate_content_idea_id(cls, value: str) -> str:
        try:
            return str(UUID(str(value)))
        except ValueError:
            raise ValueError("content_idea_id must be a valid UUID")

    @field_validator("platform")
    @classmethod
    def validate_platform(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_PLATFORMS:
            raise ValueError(f"platform must be one of: {', '.join(sorted(ALLOWED_PLATFORMS))}")
        return value

    @field_validator("post_format")
    @classmethod
    def validate_post_format(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_POST_FORMATS:
            raise ValueError(f"post_format must be one of: {', '.join(sorted(ALLOWED_POST_FORMATS))}")
        return value

    @field_validator("post_goal")
    @classmethod
    def validate_post_goal(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_POST_GOALS:
            raise ValueError(f"post_goal must be one of: {', '.join(sorted(ALLOWED_POST_GOALS))}")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content_idea_id": "CONTENT_IDEA_UUID",
                "platform": "linkedin",
                "post_format": "contrarian",
                "post_goal": "comment"
            }
        }
    )
