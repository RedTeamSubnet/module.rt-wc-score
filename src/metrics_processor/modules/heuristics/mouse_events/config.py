"""Configuration for mouse events analysis."""

from pydantic import BaseModel, Field
from .velocity import VelocityConfig
from .movement_count import MovementCountConfig
from .checkbox_path import CheckboxPathConfig


class MouseEventConfig(BaseModel):
    """Configuration for mouse event analysis."""
    class Config:
        """ Pydantic configuration."""
        frozen = True

    velocity: VelocityConfig = Field(
        default_factory=VelocityConfig, description="Velocity analysis configuration"
    )
    movement_count: MovementCountConfig = Field(
        default_factory=MovementCountConfig,
        description="Movement count analysis configuration",
    )
    checkbox_path: CheckboxPathConfig = Field(
        default_factory=CheckboxPathConfig,
        description="Checkbox path analysis configuration",
    )

