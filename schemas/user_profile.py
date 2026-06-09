from pydantic import BaseModel, ConfigDict


class CreateUserProfileRequest(BaseModel):
    id: str
    user_id: str
    niche: str
    offer: str
    target_audience: str
    expertise: str
    tone: str
    goal: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "22222222-2222-2222-2222-222222222444",
                "user_id": "11111111-1111-1111-1111-111111111111",
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
    niche: str
    offer: str
    target_audience: str
    expertise: str
    tone: str
    goal: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "niche": "AI automation for founders",
                "offer": "AI marketing workflows and systems",
                "target_audience": "early-stage founders struggling with marketing",
                "expertise": "ML engineer building AI agents",
                "tone": "bold, practical",
                "goal": "generate leads"
            }
        }
    )