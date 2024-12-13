from typing import Dict
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
    movements_count_feature_name: str = Field(
        default="mouse_movement_count",
        description="Name of the output mouse movement count feature",
    )

    class Config:
        """ Pydantic configuration."""
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
        """ Pydantic configuration."""
        frozen = True


class MouseDownUpProcessingConfig(BaseModel):
    """Processing-specific configuration for mouse down/up events."""

    feature_names: Dict[str, str] = Field(
        default={
            "mouse_downs_total": "mouse_down_total",
            "mouse_ups_total": "mouse_ups_total",
        },
        description="Names of the output features",
    )
    default_value: float = Field(
        default=None, description="Default value for invalid/missing data"
    )

    class Config:
        """ Pydantic configuration."""
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
        """ Pydantic configuration."""
        frozen = True
