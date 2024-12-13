"""Checkbox path analysis for mouse events."""

import logging
from typing import Dict, Any, Optional

from .config import CheckboxPathConfig

logger = logging.getLogger(__name__)


class CheckboxPathAnalyzer:
    """Analyzes checkbox interaction patterns for bot detection."""

    def __init__(self, config: Optional[CheckboxPathConfig] = None):
        """Initialize checkbox path analyzer."""
        self.config = config or CheckboxPathConfig()

    def _analyze_click_timing(self, time_diff: float) -> float:
        """Analyze time between checkbox clicks.

        Args:
            time_diff: Time difference between clicks in seconds

        Returns:
            Suspicion score for timing (0-1)
        """
        if time_diff < self.config.min_expected_time:
            # Too fast to be human
            return 1.0
        return 0.0

    def _analyze_path_linearity(self, linearity: float, movement_count: int) -> float:
        """Analyze path linearity between checkboxes.

        Args:
            linearity: Path linearity score (0-1)
            movement_count: Number of movements between checkboxes

        Returns:
            Suspicion score for path linearity (0-1)
        """
        if movement_count < self.config.min_movement_count:
            if linearity > self.config.max_linearity_threshold:
                # Too straight with too few movements
                return 0.9
            return 0.6  # Suspicious but not certain

        if linearity > self.config.max_linearity_threshold:
            # Very straight path even with enough movements
            return 0.7

        return 0.0

    def _analyze_distance_ratio(self, ratio: float) -> float:
        """Analyze ratio of actual path to direct distance.

        Args:
            ratio: Ratio of path distance to direct distance

        Returns:
            Suspicion score for distance ratio (0-1)
        """
        if ratio <= 1.0:
            # Perfect or near-perfect path following
            return 0.8
        elif ratio <= self.config.max_distance_ratio:
            # Suspiciously efficient path
            return 0.5
        return 0.0

    def __call__(self, features: Dict[str, Any]) -> float:
        """Analyze checkbox interaction features for bot detection.

        Args:
            features: Dictionary containing checkbox interaction features

        Returns:
            Score indicating likelihood of bot behavior (0-1, higher = more bot-like)
        """
        try:
            max_suspicion_score = 0.0
            pairs_analyzed = 0

            # Analyze each consecutive checkbox pair
            for i in range(1, 4):  # Assuming 3 checkboxes for now
                for j in range(i + 1, 4):
                    pair_key = f"checkbox_{i}_{j}"

                    time_diff = features.get(f"{pair_key}_time_diff")
                    linearity = features.get(f"{pair_key}_path_linearity")
                    distance_ratio = features.get(f"{pair_key}_distance_ratio")
                    movement_count = features.get(f"{pair_key}_movement_count")

                    if all(
                        v is not None
                        for v in [time_diff, linearity, distance_ratio, movement_count]
                    ):
                        # Calculate suspicion scores for different aspects
                        timing_score = self._analyze_click_timing(time_diff)
                        linearity_score = self._analyze_path_linearity(
                            linearity, movement_count
                        )
                        distance_score = self._analyze_distance_ratio(distance_ratio)

                        # Take the maximum suspicion score for this pair
                        pair_score = max(timing_score, linearity_score, distance_score)
                        max_suspicion_score = max(max_suspicion_score, pair_score)
                        pairs_analyzed += 1

            if pairs_analyzed == 0:
                return 0.0

            return max_suspicion_score

        except Exception as e:
            logger.error(f"Error in checkbox path analysis: {str(e)}")
            return 0.0
