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
                logger.warning("No checkbox events found")
                return {}

            return self._process_checkbox_sequence(checkboxes, mouse_movements)

        except Exception as e:
            logger.error(f"Error processing checkbox events: {str(e)}")
            return {}

    def _calculate_path_linearity(self, path: List[Dict[str, Any]]) -> tuple[float, float]:
        # Need at least 5 points for the new calculation method
        if len(path) < 5:
            return 1.0, 0.0
        points = np.array([[p["x"], p["y"]] for p in path])

        # Calculate angles between consecutive segments using 5 points
        angles = []
        for i in range(len(points) - 2):
            p1, p2, p3 = points[i : i + 3]

            # Vectors between points
            v1 = p2 - p1
            v2 = p3 - p2

            # Calculate angle between vectors
            dot_product = np.dot(v1, v2)
            norms = np.linalg.norm(v1) * np.linalg.norm(v2)

            if norms > 0:
                cos_angle = dot_product / norms
                # Ensure cos_angle is within [-1, 1] to avoid numerical errors
                cos_angle = min(1, max(-1, cos_angle))
                angle = np.arccos(cos_angle)
                angles.append(abs(angle))
            else:
                angles.append(1.0)

        # Calculate point-to-line distances
        start_point = points[0]
        end_point = points[-1]
        path_vector = end_point - start_point
        path_length = np.linalg.norm(path_vector)

        if path_length < 1e-10:  # Add small threshold
            return 0.0, 0.0

        # Calculate perpendicular distances from points to the line
        distances = []
        for point in points[1:-1]:
            v = point - start_point
            proj = np.dot(v, path_vector) / path_length
            parallel_point = start_point + (proj / path_length) * path_vector
            distance = np.linalg.norm(point - parallel_point)
            distances.append(distance)

        # Safely calculate angle consistency
        if angles:  # Check if angles list is not empty
            angle_consistency = 1 - (np.mean(angles) / np.pi)
            avg_angle = np.mean(angles)
        else:
            angle_consistency = 1.0
            avg_angle = 0.0

        # Safely calculate distance score
        if distances:  # Check if distances list is not empty
            max_allowed_distance = max(path_length * 0.1, 1e-10)  # Add minimum threshold
            distance_score = 1 - min(1, np.mean(distances) / max_allowed_distance)
        else:
            distance_score = 1.0

        # Calculate straightness with safety check
        total_segment_length = sum(
            np.linalg.norm(points[i + 1] - points[i]) for i in range(len(points) - 1)
        )

        if total_segment_length > 1e-10:  # Add small threshold
            straightness = path_length / total_segment_length
        else:
            straightness = 1.0

        # Combine scores with weights
        linearity_score = (
            0.4 * angle_consistency + 0.3 * distance_score + 0.3 * straightness
        )

        return linearity_score, avg_angle

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
        features = {
            "checkbox":[]
        }

        for i in range(len(sorted_checkboxes) - 1):
            checkbox = {}
            current = sorted_checkboxes[i]
            next_cb = sorted_checkboxes[i + 1]

            t1 = parse(current["timestamp"])
            t2 = parse(next_cb["timestamp"])

            time_diff = (t2 - t1).total_seconds()

            movements_between = [
                m for m in mouse_movements if t1 <= parse(m["timestamp"]) <= t2
            ]

            if movements_between:
                sorted_movements = sorted(
                    movements_between, key=lambda x: parse(x["timestamp"])
                )
                linearity, avg_angle_degrees = self._calculate_path_linearity(
                    sorted_movements
                )
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
            checkbox.update(
                {
                    "time_diff": time_diff,
                    "path_linearity": linearity,
                    "distance_ratio": (
                        path_distance / direct_distance if direct_distance > 0 else 1.0
                    ),
                    "movement_count": len(movements_between),
                    "avg_angle_degrees": avg_angle_degrees,
                }
            )
            features["checkbox"].append(checkbox)
        return features
