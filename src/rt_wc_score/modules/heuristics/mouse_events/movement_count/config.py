"""Configuration for movement count analysis."""

from pydantic import BaseModel, Field


class MovementCountConfig(BaseModel):
    class Config:
        """Pydantic configuration."""
        frozen = True
    min_movement_count: int = Field(
        default=50, description="Minimum expected mouse movements"
    )
    min_movement_count_too_low: int = Field(
        default=5, description="Minimum mouse movement count to consider user as bot"
    )
    max_movement_count: int = Field(
        default=800, description="Maximum expected mouse movements"
    )
    weight: float = Field(default=0.8, description="Weight for movement count analysis")

