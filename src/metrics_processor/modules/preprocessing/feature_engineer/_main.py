"""Feature engineering module for processing mouse and keyboard events."""

import logging
from typing import Dict, List, Any, Optional

from ._mouse_movement import MouseMovementProcessor
from ._mouse_down_up import MouseDownUpProcessor
from ._keyboard_events import KeyboardEventsProcessor
from .config import FeatureEngineerConfig

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """Coordinates the processing of all mouse and keyboard features."""

    def __init__(self, config: Optional[FeatureEngineerConfig] = None):
        """Initialize feature engineering processors.

        Args:
            config: Configuration for feature engineering. If None, uses defaults.
        """
        self.config = config or FeatureEngineerConfig()

        self.mouse_movement_processor = MouseMovementProcessor(
            config=self.config.mouse_movement
        )
        self.mouse_down_up_processor = MouseDownUpProcessor(
            config=self.config.mouse_down_up
        )
        self.keyboard_processor = KeyboardEventsProcessor(config=self.config.keyboard)

    def __call__(self, data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Process input data and engineer features.

        Args:
            data: Dictionary containing mouse and keyboard event data

        Returns:
            Dictionary containing engineered features
        """
        try:
            mouse_movement_results = self.mouse_movement_processor(
                data.get(self.config.mouse_movement.input_field, [])
            )

            mouse_down_up_data = {
                self.config.mouse_down_up.down_field: data.get(
                    self.config.mouse_down_up.down_field, []
                ),
                self.config.mouse_down_up.up_field: data.get(
                    self.config.mouse_down_up.up_field, []
                ),
            }
            mouse_down_up_results = self.mouse_down_up_processor(mouse_down_up_data)

            keyboard_data = {
                field_name: data.get(field_path, [])
                for field_name, field_path in self.config.keyboard.input_fields.items()
            }
            keyboard_results = self.keyboard_processor(keyboard_data)

            return {
                **mouse_movement_results,
                **mouse_down_up_results,
                **keyboard_results,
            }

        except Exception as e:
            logger.error(f"Error processing features: {str(e)}", exc_info=True)
            return {}
