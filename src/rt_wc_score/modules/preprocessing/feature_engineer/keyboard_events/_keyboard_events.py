"""Keyboard events processor for extracting event features."""

import logging
from typing import Dict, List, Optional

import numpy as np

from .._base import BaseFeatureEngineer
from .config import KeyboardConfig

logger = logging.getLogger(__name__)


class KeyboardEventsProcessor(BaseFeatureEngineer):
    """Processes keyboard events to extract count features."""

    def __init__(self, config: Optional[KeyboardConfig] = None):
        """Initialize the processor with configuration.

        Args:
            config: Configuration for keyboard events processing
        """
        self.config = config or KeyboardConfig()

    def _get_event_count(self, events: List[Dict] | None) -> float:
        """Get count of events with validation.

        Args:
            events: List of keyboard events

        Returns:
            Count of events or default value if invalid
        """
        if not isinstance(events, list):
            return self.config.processing.default_value
        return len(events)

    def __call__(self, events: Dict[str, List[Dict]]) -> Dict[str, float]:
        """Process keyboard events and compute count features.

        Args:
            events: Dictionary containing different types of keyboard events

        Returns:
            Dictionary containing computed count features
        """
        try:
            return {
                self.config.processing.feature_names[
                    "keypresses"
                ]: self._get_event_count(
                    events.get(self.config.input_fields["keypresses"])
                ),
                self.config.processing.feature_names["keydowns"]: self._get_event_count(
                    events.get(self.config.input_fields["keydowns"])
                ),
                self.config.processing.feature_names["keyups"]: self._get_event_count(
                    events.get(self.config.input_fields["keyups"])
                ),
            }
        except Exception as e:
            logger.error(f"Error processing keyboard events: {str(e)}")
            return {
                name: self.config.processing.default_value
                for name in self.config.processing.feature_names.values()
            }
