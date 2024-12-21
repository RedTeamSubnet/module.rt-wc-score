"""Checkbox path analysis for mouse events."""

import logging
import math
from typing import Dict, Any, Optional

import numpy as np
from .config import CheckboxPathConfig
from .._base import BaseHeuristicCheck
logger = logging.getLogger(__name__)


class CheckboxPathAnalyzer(BaseHeuristicCheck):
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
                    avg_angle_degrees = feature.get("avg_angle_degrees")

                    if all(
                        v is not None
                        for v in [time_diff, linearity, movement_count]
                    ):
                        timing_score = self._analyze_click_timing(time_diff)
                        linearity_score = self._analyze_path_linearity(linearity)
                        avg_angle_score = self._analyze_avg_angle(avg_angle_degrees)

                        pair_score = (
                            0.1 * timing_score
                            + 0.4 * linearity_score
                            + 0.5 * avg_angle_score
                        )
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

        score = self.scoring_function(
            value=time_diff,
            min_value=self.config.min_expected_time,
            max_value=self.config.max_expected_time,
            min_score=0.8,
            max_score=0.5,
            min_of_min=0.5,  # min_expected_time * 0.5 = 0.5
            max_of_max=2,    # max_expected_time * 2   = 8
        )

        return self.clamp_score_zero_to_one(score)

    def _analyze_path_linearity(self, linearity: float) -> float:
        """Analyze path linearity between checkboxes.

        Args:
            linearity: Path linearity score (0-1)
            movement_count: Number of movements between checkboxes

        Returns:
            Suspicion score for path linearity (0-1)
        """
        score = self.scoring_function(
            value=linearity,
            min_value=self.config.min_linearity_threshold,
            max_value=self.config.max_linearity_threshold,
            min_score=0.8,
            max_score=0.5,
            min_of_min=0.6,   # min_linearity_threshold * 0.6  = 0.45
            max_of_max=1.04,  # max_linearity_threshold * 1.04 = 0.988
        )


        return self.clamp_score_zero_to_one(score)

    def _analyze_avg_angle(self, avg_angle_degrees: float) -> float:
        """Analyze average angle between movements.

        Args:
            avg_angle_degrees: Average angle between movements in degrees

        Returns:
            Suspicion score for average angle (0-1)
        """
        score = self.scoring_function(
            value = avg_angle_degrees,
            min_value = self.config.min_avg_angle_degrees,
            max_value = self.config.max_avg_angle_degrees,
            min_score = 0.5,
            max_score = 0.8,
            min_of_min = 0.5,
            max_of_max = 1.5

        )
        return self.clamp_score_zero_to_one(score)
