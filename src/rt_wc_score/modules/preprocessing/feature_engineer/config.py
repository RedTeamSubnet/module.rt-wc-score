"""Configuration for feature engineering module."""

from pydantic import BaseModel, Field

from .keyboard_events import KeyboardConfig
from .mouse_events import MouseDownUpConfig, MouseMovementConfig
from .checkboxes import CheckboxFeatureConfig


class FeatureEngineerConfig(BaseModel):
    """Main configuration for feature engineering."""

    mouse_movement: MouseMovementConfig = Field(
        default_factory=MouseMovementConfig,
        description="Mouse movement processing configuration",
    )
    mouse_down_up: MouseDownUpConfig = Field(
        default_factory=MouseDownUpConfig,
        description="Mouse down/up processing configuration",
    )
    keyboard: KeyboardConfig = Field(
        default_factory=KeyboardConfig,
        description="Keyboard events processing configuration",
    )
    checkbox: CheckboxFeatureConfig = Field(
        default_factory=CheckboxFeatureConfig,
        description="Checkbox events processing configuration",
    )

    class Config:
        """ Pydantic configuration."""
        frozen = True
