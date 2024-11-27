"""Configuration for velocity-based analysis."""

from pydantic import BaseModel, Field


class VelocityConfig(BaseModel):
    """Configuration for velocity-based heuristics."""

    min_velocity_variation: float = Field(
        default=100.0, description="Minimum expected velocity standard deviation"
    )
    max_velocity_variation: float = Field(
        default=2000.0, description="Maximum expected velocity standard deviation"
    )
    weight: float = Field(
        default=1.0, description="Weight for velocity analysis in final score"
    )

    class Config:
        frozen = True
