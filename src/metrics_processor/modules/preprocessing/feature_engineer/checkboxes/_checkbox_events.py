"""Checkbox event feature engineering."""

import logging
from typing import Dict, List, Any, Optional
import numpy as np
from dateutil.parser import parse

from .._base import BaseFeatureEngineer
from .config import CheckboxFeatureConfig

logger = logging.getLogger(__name__)


class CheckboxEventProcessor(BaseFeatureEngineer):
    """Processes checkbox interactions to extract features."""

    def __init__(self, config: Optional[CheckboxFeatureConfig] = None):
        """Initialize the processor."""
        self.config = config or CheckboxFeatureConfig()

    def __call__(self, data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Process checkbox events and extract features.

        Args:
            data: Dictionary containing checkbox and mouse movement data

        Returns:
            Dictionary containing extracted features
        """
        try:
            checkboxes = data.get(self.config.input_field, [])
            mouse_movements = data.get("mouse_movements", [])

            if not checkboxes:
                return {}

            return self._process_checkbox_sequence(checkboxes, mouse_movements)

        except Exception as e:
            logger.error(f"Error processing checkbox events: {str(e)}")
            return {}

    def _calculate_path_linearity(self, path: List[Dict[str, Any]]) -> float:
        """Calculate how linear a path is between points.

        Args:
            path: List of points with x, y coordinates

        Returns:
            Linearity score (0-1, where 1 is perfectly linear)
        """
        if len(path) < 3:
            return 1.0  # Not enough points to determine non-linearity

        # Convert to numpy arrays for easier calculation
        points = np.array([[p["x"], p["y"]] for p in path])

        # Calculate total path length
        path_length = np.sum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))

        # Calculate direct distance between endpoints
        direct_distance = np.sqrt(np.sum((points[-1] - points[0]) ** 2))

        # Linearity score: ratio of direct distance to path length
        # Will be 1.0 for perfectly straight line, less for curved paths
        return direct_distance / path_length if path_length > 0 else 1.0

    def _process_checkbox_sequence(
        self, checkboxes: List[Dict], mouse_movements: List[Dict]
    ) -> Dict[str, Any]:
        """Process sequence of checkbox interactions.
        Args:
            checkboxes: List of checkbox interactions
            mouse_movements: List of mouse movements

        Returns:
            Dictionary of extracted features
        """
        sorted_checkboxes = sorted(checkboxes, key=lambda x: parse(x["timestamp"]))

        features = {}

        for i in range(len(sorted_checkboxes) - 1):
            current = sorted_checkboxes[i]
            next_cb = sorted_checkboxes[i + 1]

            t1 = parse(current["timestamp"])
            t2 = parse(next_cb["timestamp"])

            time_diff = (t2 - t1).total_seconds()

            movements_between = [
                m for m in mouse_movements if t1 <= parse(m["timestamp"]) <= t2
            ]

            if movements_between:
                linearity = self._calculate_path_linearity(movements_between)
            else:
                linearity = 1.0  # Default to 1 if no movements

            direct_distance = np.sqrt(
                (next_cb["x"] - current["x"]) ** 2 + (next_cb["y"] - current["y"]) ** 2
            )

            # Calculate actual path distance if we have movements
            if len(movements_between) > 1:
                path_distance = sum(
                    np.sqrt(
                        (movements_between[i + 1]["x"] - movements_between[i]["x"]) ** 2
                        + (movements_between[i + 1]["y"] - movements_between[i]["y"])
                        ** 2
                    )
                    for i in range(len(movements_between) - 1)
                )
            else:
                path_distance = direct_distance

            # Store features for this pair
            pair_key = f"checkbox_{current['checkboxId']}_{next_cb['checkboxId']}"
            features.update(
                {
                    f"{pair_key}_time_diff": time_diff,
                    f"{pair_key}_path_linearity": linearity,
                    f"{pair_key}_distance_ratio": (
                        path_distance / direct_distance if direct_distance > 0 else 1.0
                    ),
                    f"{pair_key}_movement_count": len(movements_between),
                }
            )

        # Add sequence features
        features.update(
            {
                "checkbox_interaction_sequence": "_".join(
                    str(cb["checkboxId"]) for cb in sorted_checkboxes
                ),
                "total_checkbox_time": (
                    parse(sorted_checkboxes[-1]["timestamp"])
                    - parse(sorted_checkboxes[0]["timestamp"])
                ).total_seconds(),
            }
        )

        return features
