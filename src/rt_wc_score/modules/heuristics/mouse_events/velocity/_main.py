"""Velocity analysis for mouse events."""

import math
import logging
from typing import Dict, Any, Optional

from .config import VelocityConfig
import numpy as np
logger = logging.getLogger(__name__)


class VelocityAnalyzer:
    """Analyzes mouse velocity patterns for bot detection."""

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze velocity features for bot detection."""
        try:

            stddev_velocity = features.get("mouse_movement_stddev_velocity", 0.0)
            print("stddev_velocity",stddev_velocity)
            score = round(
                self.scoring_function(
                    stddev_velocity,
                    self.config.min_velocity_variation,
                    self.config.max_velocity_variation,
                ),
                5,
            )
            return   score

        except Exception as e:
            logger.error(f"Error in velocity analysis: {str(e)}")
            return 0.0

    def __init__(self, config: Optional[VelocityConfig] = None):
        """Initialize velocity analyzer."""
        self.config = config or VelocityConfig()



    def scoring_function(self, count, min_, max_, min_score=0.80, max_score=0.65):
        if count < min_:
            distance_factor = (min_ - count) / min_
            base_score = min_score + (1 - min_score) * distance_factor
            return min(1, base_score + np.cos(count) * 0.0084)
        elif count > max_:
            distance_factor = (count - max_) / max_
            base_score = max_score + (1 - max_score) * distance_factor
            return min(1, base_score + np.cos(count) * 0.0084)
        else:
            return 0
