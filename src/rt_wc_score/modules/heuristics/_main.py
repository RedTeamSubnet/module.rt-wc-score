"""Main module for heuristic analysis."""

import logging
from typing import Dict, Any, Optional

from .config import HeuristicConfig
from .mouse_events import MouseEventAnalyzer

logger = logging.getLogger(__name__)


class HeuristicAnalyzer:
    """Main class for analyzing features using heuristics."""

    def __init__(self, config: Optional[HeuristicConfig] = None):
        """Initialize analyzers with configuration.

        Args:
            config: Configuration for heuristic analysis
        """
        self.config = config or HeuristicConfig()
        self.mouse_analyzer = MouseEventAnalyzer(config=self.config.mouse_events)

    def __call__(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze features to detect bot-like behavior.

        Args:
            features: Dictionary of engineered features

        Returns:
            Dictionary containing detection results and scores
        """
        try:
            # Get mouse event scores
            mouse_scores = self.mouse_analyzer(features)

            # Calculate final score

            final_score = round(1 - self._calculate_final_score(mouse_scores), 5)

            # Determine if it's bot-like based on threshold
            is_bot = int(final_score < self.config.score_threshold)

            # Calculate confidence based on score distance from threshold
            confidence = abs(final_score - self.config.score_threshold)

            return {
                "is_bot": is_bot,
                "confidence": min(confidence, 1.0),  # Cap confidence at 1.0
                "score": final_score,
                "mouse_scores": mouse_scores,
                "threshold_used": self.config.score_threshold,
            }

        except Exception as e:
            logger.error(f"Error in heuristic analysis: {str(e)}", exc_info=True)
            return {
                "is_bot": 1,  # Default to human on error
                "confidence": 1.0,
                "score": 0.0,
                "error": str(e),
            }

    def _calculate_final_score(self, scores: Dict[str, Dict[str, float]]) -> float:
        """Calculate weighted average score.

        Args:
            scores: Dictionary containing scores and weights

        Returns:
            Final weighted score
        """
        total_weight = 0
        weighted_sum = 0

        for analyzer_scores in scores.values():
            score = analyzer_scores.get("score", 0)
            weight = analyzer_scores.get("weight", 0)

            weighted_sum += score * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return weighted_sum / total_weight
