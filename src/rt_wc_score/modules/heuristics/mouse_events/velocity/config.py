"""Configuration for velocity-based analysis."""

from pydantic import BaseModel, Field


class VelocityConfig(BaseModel):
    min_velocity_variation: float = Field(
        default=200.0,
        description="Minimum expected velocity standard deviation",
    )
    max_velocity_variation: float = Field(
        default=3000.0,
        description="Maximum expected velocity standard deviation",
    )
    weight: float = Field(default=1.0, description="Weight for velocity analysis")

    class Config:
        frozen = True
