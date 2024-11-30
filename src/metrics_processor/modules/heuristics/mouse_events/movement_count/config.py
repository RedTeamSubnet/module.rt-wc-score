"""Configuration for movement count analysis."""

from pydantic import BaseModel, Field


class MovementCountConfig(BaseModel):
    class Config:
        """Pydantic configuration."""
        frozen = True
    min_movement_count: int = Field(
        default=15, description="Minimum expected mouse movements"
    )
    max_movement_count: int = Field(
        default=2000, description="Maximum expected mouse movements"
    )
    weight: float = Field(default=0.8, description="Weight for movement count analysis")

