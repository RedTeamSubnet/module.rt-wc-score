"""Velocity analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .config import VelocityConfig

logger = logging.getLogger(__name__)


class VelocityAnalyzer:
    """Analyzes mouse velocity patterns for bot detection."""

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze velocity features for bot detection."""
        try:
            stddev_velocity = features.get("mouse_movement_stddev_velocity", 0.0)

            if stddev_velocity == 0:
                return 1.0  # Perfect constant velocity is suspicious

            if stddev_velocity < self.config.min_velocity_variation:
                return 0.8  # Too constant velocity
            elif stddev_velocity > self.config.max_velocity_variation:
                return 0.6  # Too erratic velocity

            return 0.0

        except Exception as e:
            logger.error(f"Error in velocity analysis: {str(e)}")
            return 0.0

    def __init__(self, config: Optional[VelocityConfig] = None):
        """Initialize velocity analyzer."""
        self.config = config or VelocityConfig()
