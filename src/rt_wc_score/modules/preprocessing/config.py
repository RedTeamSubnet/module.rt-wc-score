"""Configuration for preprocessing module."""

from pydantic import BaseModel, Field

from .json_flattener.config import JsonDataFlattenerConfigPM
from .feature_engineer.config import FeatureEngineerConfig


class PreprocessorConfig(BaseModel):
    """Configuration for preprocessing pipeline."""

    flattener: JsonDataFlattenerConfigPM = Field(
        default_factory=JsonDataFlattenerConfigPM,
        description="Configuration for JSON flattening",
    )
    feature_engineer: FeatureEngineerConfig = Field(
        default_factory=FeatureEngineerConfig,
        description="Configuration for feature engineering",
    )

    class Config:
        frozen = True
