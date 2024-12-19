"""Movement count analysis for mouse events."""
import math
import logging
from typing import Dict, Any, Optional

from .config import MovementCountConfig

logger = logging.getLogger(__name__)


class MovementCountAnalyzer:
    """Analyzes mouse movement count for bot detection."""

    def __init__(self, config: Optional[MovementCountConfig] = None):
        """Initialize movement count analyzer."""
        self.config = config or MovementCountConfig()

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze movement count for bot detection."""
        try:

            movement_count = features.get("mouse_movement_count", 0)
            score = self.give_scaling_score(
                movement_count,
                self.config.min_movement_count,
                self.config.max_movement_count,
            )
            score = round(score, 5)
            return score
            # if movement_count < self.config.min_movement_count_hard:
            #     return 1.0  # Too few   100% botness score
            # if movement_count < self.config.min_movement_count:
            #     return 0.7  # Too few movements
            # elif movement_count > self.config.max_movement_count:
            #     return 0.8  # Suspiciously high number of movements

            # return 0.0

        except Exception as e:
            logger.error(f"Error in movement count analysis: {str(e)}")
            return 0.0

    def give_scaling_score(self,
        value, min_val, max_val, growth_rate_min=0.3, growth_rate_max=0.03
    ):
        if min_val < value < max_val:
            return 0  # Value is within the range
        if value < min_val:
            distance = min_val - value
            return 1 - math.exp(-growth_rate_min * distance)
        if value > max_val:
            distance = value - max_val
            return 1 - math.exp(-growth_rate_max * distance)
