"""Main preprocessing module combining flattening and feature engineering."""

import logging
from typing import Dict, Any, Optional, Union

from .json_flattener import JsonDataFlattener
from .feature_engineer import FeatureEngineer
from .config import PreprocessorConfig

logger = logging.getLogger(__name__)


class Preprocessor:
    """Main preprocessing class that handles data flattening and feature engineering."""

    def __init__(self, config: Optional[PreprocessorConfig] = None):
        """Initialize the preprocessor with configurations.

        Args:
            config: Configuration for preprocessing pipeline
        """
        self.config = config or PreprocessorConfig()

        # Initialize sub-processors
        self.flattener = JsonDataFlattener(config=self.config.flattener)
        self.feature_engineer = FeatureEngineer(config=self.config.feature_engineer)

    def __call__(self, data: Union[str, Dict]) -> Optional[Dict[str, Any]]:
        """Process input data through flattening and feature engineering.

        Args:
            data: Input data either as JSON string or dictionary

        Returns:
            Dictionary containing engineered features or None if processing fails
        """
        try:
            # Step 1: Flatten the data
            logger.info("Flattening input data...")
            flattened_data = self.flattener(data)

            if flattened_data is None:
                logger.error("Failed to flatten input data")
                return None

            # Step 2: Engineer features
            logger.info("Engineering features...")
            features = self.feature_engineer(flattened_data)

            if not features:
                logger.error("Failed to engineer features")
                return None
            features["user_id"] = flattened_data["user_id"]
            features["project_id"] = flattened_data["project_id"]
            return features

        except Exception as e:
            logger.error(f"Error during preprocessing: {str(e)}", exc_info=True)
            return None
