"""Configuration for preprocessing module."""

from pydantic import BaseModel, Field

from .json_flattener.config import JsonDataFlattenerConfigPM
from .feature_engineer.config import FeatureEngineerConfig


class PreprocessorConfig(BaseModel):
    """Configuration for preprocessing pipeline."""
    class Config:
        """ Pydantic model configuration."""
        frozen = True

    flattener: JsonDataFlattenerConfigPM = Field(
        default_factory=JsonDataFlattenerConfigPM,
        description="Configuration for JSON flattening",
    )
    feature_engineer: FeatureEngineerConfig = Field(
        default_factory=FeatureEngineerConfig,
        description="Configuration for feature engineering",
    )
