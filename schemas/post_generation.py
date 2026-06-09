from pydantic import BaseModel, ConfigDict

class GeneratePostRequest(BaseModel):
    content_idea_id: str
    platform: str
    post_format: str
    post_goal: str

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