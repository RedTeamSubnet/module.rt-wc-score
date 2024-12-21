"""Movement count analysis for mouse events."""
import logging
from typing import Dict, Any, Optional

from .._base import BaseHeuristicCheck

from .config import MovementCountConfig

logger = logging.getLogger(__name__)


class MovementCountAnalyzer(BaseHeuristicCheck):
    """Analyzes mouse movement count for bot detection."""

    def __init__(self, config: Optional[MovementCountConfig] = None):
        """Initialize movement count analyzer."""
        self.config = config or MovementCountConfig()

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze movement count for bot detection."""
        try:

            movement_count = features.get("mouse_movement_count", 0)
            if movement_count < self.config.min_movement_count_too_low:
                return 1.0
            score = self.scoring_function(
                value = movement_count,
                min_value=self.config.min_movement_count,
                max_value=self.config.max_movement_count,
                min_score=0.6,
                max_score=0.65,
                min_of_min=0.2,
                max_of_max=1.5,
            )
            score = round(score, 5)
            return self.clamp_score_zero_to_one(score)
        except Exception as e:
            logger.error(f"Error in movement count analysis: {str(e)}")
            return 0.0
