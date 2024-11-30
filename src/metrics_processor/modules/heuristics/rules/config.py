"""Configuration for rule combination."""

from pydantic import BaseModel, Field


class RuleConfig(BaseModel):
    """Configuration for rule combination."""
    class Config:
        """ Pydantic configuration."""
        frozen = True

    combination_method: str = Field(
        default="weighted_average", description="Method to combine individual scores"
    )
    min_rules_required: int = Field(
        default=2, description="Minimum number of rules needed for valid classification"
    )
    confidence_threshold: float = Field(
        default=0.7, description="Minimum confidence needed for classification"
    )

