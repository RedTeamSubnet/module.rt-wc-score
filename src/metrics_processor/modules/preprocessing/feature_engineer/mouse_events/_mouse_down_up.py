"""Mouse down/up processor for extracting timing features."""

import logging
from typing import Dict, List, Any, Optional

from .._base import BaseFeatureEngineer
from .config import MouseDownUpConfig

logger = logging.getLogger(__name__)


class MouseDownUpProcessor(BaseFeatureEngineer):
    """Processes mouse down/up events to extract timing features."""

    def __init__(self, config: Optional[MouseDownUpConfig] = None):
        """Initialize the processor with configuration.

        Args:
            config: Configuration for mouse down/up processing
        """
        self.config = config or MouseDownUpConfig()

    def _get_default_results(self) -> Dict[str, Any]:
        """Get dictionary of default feature values.

        Returns:
            Dictionary with default values for all features
        """
        return {
            feature_name: self.config.processing.default_value
            for feature_name in self.config.processing.feature_names.values()
        }

    def __call__(self, mouse_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Process mouse down/up events and compute timing features.

        Args:
            mouse_data: Dictionary containing mouse down and up events

        Returns:
            Dictionary containing computed features
        """
        try:
            results = self._get_default_results()
            results[self.config.processing.feature_names["downs_total"]] = len(
                mouse_data.get(self.config.down_field, [])
            )
            results[self.config.processing.feature_names["ups_total"]] = len(
                mouse_data.get(self.config.up_field, [])
            )

            return results

        except Exception as e:
            logger.error(f"Error processing mouse down/up events: {str(e)}")
            return self._get_default_results()
