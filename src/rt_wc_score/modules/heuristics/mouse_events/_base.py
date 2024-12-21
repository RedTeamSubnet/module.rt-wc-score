import logging
import math

from typing import Any
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class BaseHeuristicCheck(ABC):

    """Abstract base class for data preprocessing."""

    @abstractmethod
    def __call__(self, data: Any) -> Any:
        """Process the input data."""
        pass

    def scoring_function(self,value, min_value, max_value, min_score=0.40, max_score=0.40,min_of_min=0.3,max_of_max=1.5):
        """
        Calculate a score based on a value's relationship to specified minimum and maximum thresholds.

        The scoring function implements a sliding scale that penalizes values outside a defined range:
        - For values below min_value: Score increases from min_score till min_of_min * min_value.
        - For values above max_value: Score increases from max_score till max_of_max * max_value.
        - After passing **_of_** values the score is 1.
        - For values within range: Returns 0

        Args:
            value : float
                The input value to be scored
            min_value : float
                Lower threshold value
            max_value : float
                Upper threshold value
            min_score : float, optional
                Base score for values below min_value (default: 0.40)
            max_score : float, optional
                Base score for values above max_value (default: 0.40)
            min_of_min : float, optional
                Multiplier for absolute minimum value (default: 0.3)
            max_of_max : float, optional
                Multiplier for absolute maximum value (default: 1.5)

        Returns:
            float
                Normalized score between 0 and 1
        """

        if value < min_value:
            score = min_score + (1 - min_score) * self.inverse_scaling(
                value, min_of_min*min_value, min_value, 0.05, 1, 0.1
            )
            return min(1,score)
        elif value > max_value:
            score = max_score + (1 - max_score) * self.inverse_scaling(
                value, max_value, max_of_max * max_value, 0.95, 0.05, 0.1
            ) # min and max changed to inverse `inverse_scaling`
            return min(1,score)
        else:
            return 0

    def inverse_scaling(self,value, min_input, max_input, min_value, max_value, rate=1.0):
        """
        Returns a scaled value inversely proportional to the input.

        Args:
        - value: Input value to scale.
        - min_input: Minimum input value.
        - max_input: Maximum input value.
        - min_value: Minimum output value.
        - max_value: Maximum output value.
        - rate: Growth rate of the exponential scaling (default=1.0).

        Returns:
        - Scaled output between min_value and max_value.
        """

        normalized = (value - min_input) / (max_input - min_input)
        scaled = math.exp(-rate * normalized)
        scaled = (scaled - math.exp(-rate)) / (1 - math.exp(-rate))
        return min_value + scaled * (max_value - min_value)

    def clamp_score_zero_to_one(self, score):
        """
        Clamps a score value to ensure it falls within the range [0.0, 1.0].

        Args:
            score (float): Input score value to be clamped.

        Returns:
            float: Score value clamped between 0.0 and 1.0.
        """
        return max(0.0, min(1.0, score))
