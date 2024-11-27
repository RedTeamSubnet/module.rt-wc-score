"""Configuration for feature engineering module."""

from typing import Dict, List
from pydantic import BaseModel, Field


class MouseMovementProcessingConfig(BaseModel):
    """Processing-specific configuration for mouse movement analysis."""

    min_movements_required: int = Field(
        default=2,
        description="Minimum number of movements required to compute velocity",
    )
    fields: dict = Field(
        default={"x": "x", "y": "y", "timestamp": "timestamp"},
        description="Field names in the movement data",
    )
    velocity_feature_name: str = Field(
        default="mouse_movement_stddev_velocity",
        description="Name of the output velocity feature",
    )

    class Config:
        frozen = True


class MouseMovementConfig(BaseModel):
    """Complete configuration for mouse movement module."""

    input_field: str = Field(
        default="mouse_movements", description="Field name for mouse movement data"
    )
    processing: MouseMovementProcessingConfig = Field(
        default_factory=MouseMovementProcessingConfig,
        description="Processing-specific configuration",
    )

    class Config:
        frozen = True


class MouseDownUpProcessingConfig(BaseModel):
    """Processing-specific configuration for mouse down/up events."""

    feature_names: Dict[str, str] = Field(
        default={
            "mean_dwell_time": "mouse_mean_dwell_time",
            "std_dwell_time": "mouse_std_dwell_time",
            "mean_inter_click": "mouse_mean_inter_click_interval",
            "std_inter_click": "mouse_std_inter_click_interval",
            "downs_total": "mouse_mouseDowns_total",
            "ups_total": "mouse_mouseUps_total",
            "event_density": "mouse_event_density",
        },
        description="Names of the output features",
    )
    default_value: float = Field(
        default=float("nan"), description="Default value for invalid/missing data"
    )

    class Config:
        frozen = True


class MouseDownUpConfig(BaseModel):
    """Complete configuration for mouse down/up module."""

    down_field: str = Field(
        default="mouse_mouseDowns", description="Field name for mouse down events"
    )
    up_field: str = Field(
        default="mouse_mouseUps", description="Field name for mouse up events"
    )
    processing: MouseDownUpProcessingConfig = Field(
        default_factory=MouseDownUpProcessingConfig,
        description="Processing-specific configuration",
    )

    class Config:
        frozen = True


class KeyboardProcessingConfig(BaseModel):
    """Processing-specific configuration for keyboard events."""

    feature_names: Dict[str, str] = Field(
        default={
            "keypresses": "keypresses_count",
            "keydowns": "keydowns_count",
            "keyups": "keyups_count",
        },
        description="Names of the output count features",
    )
    default_value: float = Field(
        default=float("nan"), description="Default value for invalid/missing data"
    )

    class Config:
        frozen = True


class KeyboardConfig(BaseModel):
    """Complete configuration for keyboard events module."""

    input_fields: Dict[str, str] = Field(
        default={
            "keypresses": "keyboard_keypresses",
            "keydowns": "keyboard_keydowns",
            "keyups": "keyboard_keyups",
        },
        description="Field names for keyboard event data",
    )
    processing: KeyboardProcessingConfig = Field(
        default_factory=KeyboardProcessingConfig,
        description="Processing-specific configuration",
    )

    class Config:
        frozen = True


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

    class Config:
        frozen = True
