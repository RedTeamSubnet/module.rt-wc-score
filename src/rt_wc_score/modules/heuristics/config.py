"""Configuration for heuristic analysis module."""

from pydantic import BaseModel, Field
from .mouse_events.config import MouseEventConfig


class HeuristicConfig(BaseModel):
    """Main configuration for heuristic analysis."""

    class Config:
        """ Pydantic configuration."""
        frozen = True

    mouse_events: MouseEventConfig = Field(
        default_factory=MouseEventConfig,
        description="Configuration for mouse event analysis",
    )
    score_threshold: float = Field(
        default=0.35, description="Threshold for bot classification (>threshold = bot)"
    )
