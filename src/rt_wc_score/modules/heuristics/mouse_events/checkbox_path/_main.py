"""Checkbox path analysis for mouse events."""

import logging
import math
from typing import Dict, Any, Optional

import numpy as np
from .config import CheckboxPathConfig

logger = logging.getLogger(__name__)


class CheckboxPathAnalyzer:
    """Analyzes checkbox interaction patterns for bot detection."""

    def __init__(self, config: Optional[CheckboxPathConfig] = None):
        """Initialize checkbox path analyzer."""
        self.config = config or CheckboxPathConfig()

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
            if features.get("is_valid"):
                for feature in features["checkbox"]:
                    movement_count = feature.get("movement_count")
                    if movement_count < self.config.min_movement_count_too_low:
                        max_suspicion_score = 1
                        continue
                    time_diff = feature.get("time_diff")
                    linearity = feature.get("path_linearity")
                    distance_ratio = feature.get("distance_ratio")
                    avg_angle_degrees = feature.get("avg_angle_degrees")

                    if all(
                        v is not None
                        for v in [time_diff, linearity, distance_ratio, movement_count]
                    ):
                        timing_score = self._analyze_click_timing(time_diff)
                        linearity_score = self._analyze_path_linearity(linearity)
                        # distance_score = self._analyze_distance_ratio(distance_ratio) # ignoring  for now
                        avg_angle_score = self._analyze_avg_angle(avg_angle_degrees)

                        pair_score = (
                            0.1 * timing_score
                            + 0.4 * linearity_score
                            + 0.5 * avg_angle_score
                        )
                        # distance_score,
                        max_suspicion_score = max(max_suspicion_score, pair_score)
                        pairs_analyzed += 1

                if pairs_analyzed == 0:
                    return 1.0

                return max_suspicion_score
            else:

                return 1.0

        except Exception as e:
            logger.error(f"Error in checkbox path analysis: {str(e)}")
            return 0.0

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

    def _analyze_path_linearity(self, linearity: float) -> float:
        """Analyze path linearity between checkboxes.

        Args:
            linearity: Path linearity score (0-1)
            movement_count: Number of movements between checkboxes

        Returns:
            Suspicion score for path linearity (0-1)
        """
        linearity_score = self.scoring_function_max(
            linearity, self.config.max_linearity_threshold, 0.8
        )
        return linearity_score

    def _analyze_avg_angle(self, avg_angle_degrees: float) -> float:
        """Analyze average angle between movements.

        Args:
            avg_angle_degrees: Average angle between movements in degrees

        Returns:
            Suspicion score for average angle (0-1)
        """
        score = self.scoring_function(
            avg_angle_degrees,
            self.config.min_avg_angle_degrees,
            self.config.max_avg_angle_degrees,
            0.8,
            0.65,
        )
        return score

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

    def scoring_function(
        self, value, min_val, max_val, growth_rate_min=0.003, growth_rate_max=0.003
    ):
        if value == 0.0 or value ==  1.0:
            return 1
        elif min_val < value < max_val:
            return 0  # Value is within the range
        elif value < min_val:
            distance_factor = (min_val - value) / min_val
            base_score = growth_rate_min + (1 - growth_rate_min) * distance_factor
            return min(1, base_score + np.cos(value) * 0.000001)
        elif value > max_val:
            distance_factor = (value - max_val) / max_val
            base_score = growth_rate_max + (1 - growth_rate_max) * distance_factor
            return min(1, base_score + np.cos(value) * 0.000001)

    def scoring_function_max(self, value, max_, max_score=0.80):
        if value >= 1:
            return 1
        if value > max_:
            distance_factor = (max_ - value) / max_
            base_score = max_score + (1 - max_score) * distance_factor
            return min(1, base_score + np.cos(value) * 0.05)
        elif value == max_:
            return max_score
        else:
            return 0
