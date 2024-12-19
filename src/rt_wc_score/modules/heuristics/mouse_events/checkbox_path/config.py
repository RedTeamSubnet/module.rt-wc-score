"""Configuration for checkbox path analysis."""

from pydantic import BaseModel, Field


class CheckboxPathConfig(BaseModel):
    min_expected_time: float = Field(
        default=0.3,  # Reduced from 0.5 since checkboxes are visual targets
        description="Minimum expected time between checkbox clicks (seconds)",
    )
    max_linearity_threshold: float = Field(
        default=0.85, description="Threshold for suspiciously linear paths"
    )
    min_movement_count: int = Field(
        default=20, description="Minimum expected movements between checkboxes"
    )
    max_distance_ratio: float = Field(
        default=1.4, description="Maximum ratio of path distance to direct distance"
    )
    weight: float = Field(
        default=1.5,  # Increased weight as this is a key indicator
        description="Weight for checkbox path analysis",
    )
