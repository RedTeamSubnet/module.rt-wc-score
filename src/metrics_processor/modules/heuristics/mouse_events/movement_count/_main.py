"""Movement count analysis for mouse events."""

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

            if movement_count < self.config.min_movement_count:
                return 0.7  # Too few movements
            elif movement_count > self.config.max_movement_count:
                return 0.8  # Suspiciously high number of movements

            return 0.0

        except Exception as e:
            logger.error(f"Error in movement count analysis: {str(e)}")
            return 0.0
