"""Mouse movement processor for extracting velocity features."""

import logging
from typing import Dict, List, Optional

import numpy as np
from dateutil.parser import parse

from .._base import BaseFeatureEngineer
from .config import MouseMovementConfig

logger = logging.getLogger(__name__)


class MouseMovementProcessor(BaseFeatureEngineer):
    """Processes mouse movement data to extract velocity features."""

    def __init__(self, config: Optional[MouseMovementConfig] = None):
        """Initialize the processor with configuration."""
        self.config = config or MouseMovementConfig()

    def __call__(self, mouse_movement_data: List[Dict]) -> Dict[str, float]:
        """Process mouse movement data and compute velocity features."""
        try:
            velocities = self._compute_velocity(mouse_movement_data)
            count = self._compute_count(mouse_movement_data)
            return {
                self.config.processing.velocity_feature_name: (
                    np.std(velocities) if velocities else np.nan
                ),
                self.config.processing.movements_count_feature_name: count,
            }
        except Exception as e:
            logger.error(f"Error computing mouse movement features: {str(e)}")
            return {self.config.processing.velocity_feature_name: np.nan}

    def _parse_timestamp(self, timestamp_str: str) -> float:
        """Parse timestamp string to float."""
        try:
            if isinstance(timestamp_str, (int, float)):
                return float(timestamp_str)
            return parse(timestamp_str).timestamp()
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing timestamp {timestamp_str}: {str(e)}")
            return np.nan

    def _compute_velocity(self, mouse_movements: List[Dict]) -> List[float]:
        """Compute velocities from mouse movement data."""
        if not mouse_movements:
            logger.warning("Empty mouse movement data to compute velocity")
            return []

        try:
            valid_movements = [m for m in mouse_movements if m is not None]

            if len(valid_movements) < self.config.processing.min_movements_required:
                return []

            x_coords = np.array(
                [m.get(self.config.processing.fields["x"]) for m in valid_movements]
            )
            y_coords = np.array(
                [m.get(self.config.processing.fields["y"]) for m in valid_movements]
            )
            timestamps = np.array(
                [
                    self._parse_timestamp(
                        m.get(self.config.processing.fields["timestamp"])
                    )
                    for m in valid_movements
                ]
            )

            if (
                np.isnan(x_coords).any()
                or np.isnan(y_coords).any()
                or np.isnan(timestamps).any()
            ):
                logger.warning("Invalid values found in movement data")
                return []

            dx = np.diff(x_coords)
            dy = np.diff(y_coords)
            dt = np.diff(timestamps)

            distances = np.sqrt(dx**2 + dy**2)
            velocities = np.divide(
                distances, dt, out=np.zeros_like(distances), where=dt != 0
            )

            return velocities.tolist()

        except Exception as e:
            logger.error(f"Error in velocity computation: {str(e)}")
            return []

    def _compute_count(self, mouse_movements: List[Dict]) -> List[float]:
        """Compute velocities from mouse movement data."""
        if not mouse_movements:
            logger.warning("Empty mouse movement data to compute count")
            return []
        else:
            return len(mouse_movements)
