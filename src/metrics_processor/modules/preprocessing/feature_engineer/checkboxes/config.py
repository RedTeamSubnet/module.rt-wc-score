"""Configuration for checkbox event feature engineering."""

from pydantic import BaseModel, Field


class CheckboxFeatureConfig(BaseModel):
    """Configuration for checkbox feature engineering."""

    input_field: str = Field(
        default="checkboxes", description="Field name for checkbox interactions"
    )

    class Config:
        """ Pydantic configuration."""
        frozen = True
