"""Configuration for movement count analysis."""

from pydantic import BaseModel, Field


class MovementCountConfig(BaseModel):
    """Configuration for movement count heuristics."""

    min_movement_count: int = Field(
        default=10, description="Minimum expected mouse movements"
    )
    max_movement_count: int = Field(
        default=1000, description="Maximum expected mouse movements"
    )
    weight: float = Field(
        default=1.0, description="Weight for movement count analysis in final score"
    )

    class Config:
        frozen = True
