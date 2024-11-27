from typing import Dict, List
from pydantic import BaseModel, Field


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
