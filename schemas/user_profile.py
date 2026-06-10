from pydantic import BaseModel, ConfigDict


class CreateUserProfileRequest(BaseModel):
    id: str
    profile_name: str
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