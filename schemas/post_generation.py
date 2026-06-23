from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator, model_validator


ALLOWED_PLATFORMS = {"instagram", "linkedin"}
ALLOWED_INSTAGRAM_CONTENT_TYPES = {"carousel", "story", "reel"}
ALLOWED_POST_LENGTHS = {"short", "medium", "long"}
ALLOWED_POST_GOALS = {
    "comment",
    "dm_keyword",
    "follow",
    "download",
    "share",
    "save",
    "book_visit",
    "buy_order",
}


class GeneratePostRequest(BaseModel):
    content_idea_id: str
    platform: str
    post_goal: str
    instagram_content_type: Optional[str] = None
    post_length: str = "medium"

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

    @field_validator("post_goal")
    @classmethod
    def validate_post_goal(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_POST_GOALS:
            raise ValueError(f"post_goal must be one of: {', '.join(sorted(ALLOWED_POST_GOALS))}")
        return value

    @field_validator("instagram_content_type")
    @classmethod
    def validate_instagram_content_type(cls, value: Optional[str]) -> Optional[str]:
        if value is None or str(value).strip() == "":
            return None

        value = value.strip().lower()
        if value not in ALLOWED_INSTAGRAM_CONTENT_TYPES:
            raise ValueError(
                "instagram_content_type must be one of: "
                f"{', '.join(sorted(ALLOWED_INSTAGRAM_CONTENT_TYPES))}"
            )
        return value

    @field_validator("post_length")
    @classmethod
    def validate_post_length(cls, value: str) -> str:
        value = value.strip().lower()
        if value not in ALLOWED_POST_LENGTHS:
            raise ValueError(f"post_length must be one of: {', '.join(sorted(ALLOWED_POST_LENGTHS))}")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content_idea_id": "CONTENT_IDEA_UUID",
                "platform": "instagram",
                "instagram_content_type": "carousel",
                "post_goal": "comment",
                "post_length": "medium"
            }
        }
    )


class UpdatePostRequest(BaseModel):
    hook: str
    body: str
    cta: str
    final_text: str

    @model_validator(mode="after")
    def clean_text_fields(self):
        self.hook = self.hook.strip()
        self.body = self.body.strip()
        self.cta = self.cta.strip()
        self.final_text = self.final_text.strip()

        if not self.hook:
            raise ValueError("hook is required")
        if not self.final_text:
            raise ValueError("final_text is required")

        return self
