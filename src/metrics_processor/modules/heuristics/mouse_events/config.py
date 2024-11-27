"""Configuration for mouse events analysis."""

from pydantic import BaseModel, Field
from .velocity.config import VelocityConfig
from .movement_count.config import MovementCountConfig


class MouseEventConfig(BaseModel):
    """Configuration for mouse event analysis."""

    velocity: VelocityConfig = Field(
        default_factory=VelocityConfig, description="Velocity analysis configuration"
    )
    movement_count: MovementCountConfig = Field(
        default_factory=MovementCountConfig,
        description="Movement count analysis configuration",
    )

    class Config:
        frozen = True
