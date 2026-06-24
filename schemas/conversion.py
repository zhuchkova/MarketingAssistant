from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator


class CreateConversionFlowRequest(BaseModel):
    lead_magnet_id: Optional[str] = None
    custom_offer_title: Optional[str] = None
    custom_offer_url: Optional[str] = None
    custom_offer_description: Optional[str] = None

    @field_validator("lead_magnet_id")
    @classmethod
    def validate_lead_magnet_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None or str(value).strip() == "":
            return None
        try:
            return str(UUID(str(value)))
        except ValueError:
            raise ValueError("lead_magnet_id must be a valid UUID")

    @field_validator("custom_offer_title", "custom_offer_url", "custom_offer_description")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lead_magnet_id": "55555555-5555-5555-5555-555555555555",
                "custom_offer_title": None,
                "custom_offer_url": None,
                "custom_offer_description": None
            }
        }
    )
