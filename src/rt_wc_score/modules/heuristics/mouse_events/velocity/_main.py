"""Velocity analysis for mouse events."""

import math
import logging
from typing import Dict, Any, Optional
from .._base import BaseHeuristicCheck
from .config import VelocityConfig
import numpy as np

logger = logging.getLogger(__name__)


class VelocityAnalyzer(BaseHeuristicCheck):
    """Analyzes mouse velocity patterns for bot detection."""

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze velocity features for bot detection."""
        try:

            stddev_velocity = features.get("mouse_movement_stddev_velocity", 0.0)
            score = round(
                self.scoring_function(
                    value=stddev_velocity,
                    min_value= self.config.min_velocity_variation,
                    max_value= self.config.max_velocity_variation,
                    min_score= 0.6,
                    max_score= 0.4,
                    min_of_min=0.3,
                    max_of_max=1.5
                ),
                5,
            )
            return self.clamp_score_zero_to_one(score)

        except Exception as e:
            logger.error(f"Error in velocity analysis: {str(e)}")
            return 0.0

    def __init__(self, config: Optional[VelocityConfig] = None):
        """Initialize velocity analyzer."""
        self.config = config or VelocityConfig()


