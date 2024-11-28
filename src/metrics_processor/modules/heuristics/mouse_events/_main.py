"""Mouse event analysis module."""

import logging
from typing import Dict, Any, Optional

from .config import MouseEventConfig
from .velocity import VelocityAnalyzer
from .movement_count import MovementCountAnalyzer
from .checkbox_path import CheckboxPathAnalyzer

logger = logging.getLogger(__name__)


class MouseEventAnalyzer:
    """Analyzes mouse events for bot-like behavior."""

    def __init__(self, config: Optional[MouseEventConfig] = None):
        """Initialize mouse event analyzers."""
        self.config = config or MouseEventConfig()

        self.velocity_analyzer = VelocityAnalyzer(config=self.config.velocity)
        self.movement_count_analyzer = MovementCountAnalyzer(
            config=self.config.movement_count
        )
        self.checkbox_path_analyzer = CheckboxPathAnalyzer(
            config=self.config.checkbox_path
        )

    def __call__(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mouse features for bot detection."""
        try:
            velocity_score = self.velocity_analyzer(features)
            movement_count_score = self.movement_count_analyzer(features)
            checkbox_path_score = self.checkbox_path_analyzer(features)

            return {
                "velocity": {
                    "score": velocity_score,
                    "weight": self.config.velocity.weight,
                },
                "movement_count": {
                    "score": movement_count_score,
                    "weight": self.config.movement_count.weight,
                },
                "checkbox_path": {
                    "score": checkbox_path_score,
                    "weight": self.config.checkbox_path.weight,
                },
            }

        except Exception as e:
            logger.error(f"Error in mouse event analysis: {str(e)}")
            return {
                "velocity": {"score": 0.0, "weight": 0.0},
                "movement_count": {"score": 0.0, "weight": 0.0},
                "checkbox_path": {"score": 0.0, "weight": 0.0},
                "error": str(e),
            }
