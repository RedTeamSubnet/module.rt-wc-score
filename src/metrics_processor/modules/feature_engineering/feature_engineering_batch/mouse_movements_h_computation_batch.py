import logging
import math

import numpy as np
import pandas as pd
logger = logging.getLogger(__name__)
from .feature_engineering_batch import FeatureEngineeringBatch  # noqa: E402
# from  import is_nan  # noqa: E402


def is_nan(feature_name, value):
    if value is None:
        # log_error(f'ignoring nan value in {feature_name}:{value}')
        return True
    if isinstance(value, float) and math.isnan(value):
        # log_error(f"ignored NaN value in {feature_name}:{value}")
        return True
    elif isinstance(value, pd.Series) and value.isna().any():
        # nan_indices = value.index[value.isna()]
        # for index in nan_indices:
        # log_error(f"NaN value found for feature '{feature_name}' at index '{index}'")
        return True
    # else:
    return False


class MouseMovementsHComputationBatch(FeatureEngineeringBatch):
    _threshold_factor = 2.0
    _absolute_threshold = 1 * 10**7
    def __init__(self, threshold_factor=2.0, absolute_threshold=1 * 10**7) -> None:
        super().__init__()
        self._threshold_factor = threshold_factor
        self._absolute_threshold = absolute_threshold

    def process(self, mouse_data: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame(index=mouse_data.index)

        result["UM_ui_mouseMovements_count"] = mouse_data[
            "UM_ui_mouseMovements_list"
        ].apply(self._count_mouse_movement)
        result["UM_ui_mouseMovements_acceleration_peaks"] = mouse_data.apply(
            self._detect_acceleration_peaks, axis=1
        )

        # result['vel_acc_xy'] = mouse_data['UM_ui_mouseMovements_list'].apply(
        #     self._calculate_velocities_and_acceleration)
        # result = pd.concat([result.drop(['vel_acc_xy'], axis=1),
        #                     result['vel_acc_xy'].apply(pd.Series)], axis=1)
        # Calculate velocities and acceleration in a single step without double apply
        velocities_and_acceleration = mouse_data["UM_ui_mouseMovements_list"].map(
            self._calculate_velocities_and_acceleration
        )

        # Convert the list of dictionaries to a DataFrame and concatenate with the result
        velocities_and_acceleration_df = pd.DataFrame(
            velocities_and_acceleration.tolist(), index=mouse_data.index
        )
        result = pd.concat([result, velocities_and_acceleration_df], axis=1)
        result["UM_ui_mouseMovements_vel_x_std"] = result["vel_x"].apply(
            lambda x: np.nanstd(x) if x else np.nan
        )
        result["UM_ui_mouseMovements_vel_y_std"] = result["vel_y"].apply(
            lambda x: np.nanstd(x) if x else np.nan
        )

        result["UM_ui_mouseMovements_self_intersections"] = mouse_data[
            "UM_ui_mouseMovements_list"
        ].apply(self._calculate_self_intersections)

        result["UM_ui_mouseMovements_angles"] = mouse_data[
            "UM_ui_mouseMovements_list"
        ].apply(self._calculate_movement_angles)
        result["UM_ui_mouseMovements_angles_std"] = result[
            "UM_ui_mouseMovements_angles"
        ].apply(self._calculate_angles_std)

        result["UM_ui_mouseMovements_elapsed_time"] = mouse_data[
            "UM_ui_mouseMovements_list"
        ].apply(self._calculate_elapsed_time)

        result["UM_ui_mouseMovements_normalized"] = mouse_data.apply(
            self._apply_normalization, axis=1
        )
        result["UM_ui_mouseMovements_length_ratio"] = result[
            "UM_ui_mouseMovements_normalized"
        ].apply(self._calculate_length_ratio)

        result = result.drop(columns=["vel_x", "vel_y", "acc_x", "acc_y"])

        return result

    def _count_mouse_movement(self, mouse_data):
        return len(mouse_data) if isinstance(mouse_data, list) else 0

    def _detect_acceleration_peaks(self, row):
        mean = (
            row["UM_ui_mouseMovements_mean_acceleration"]
            if not np.isnan(row["UM_ui_mouseMovements_mean_acceleration"])
            else 0
        )
        stddev = (
            row["UM_ui_mouseMovements_stddev_acceleration"]
            if not np.isnan(row["UM_ui_mouseMovements_stddev_acceleration"])
            else 0
        )
        pos_threshold = (
            mean + self._threshold_factor * stddev
            if self._absolute_threshold is None
            else self._absolute_threshold
        )
        neg_threshold = (
            mean - self._threshold_factor * stddev
            if self._absolute_threshold is None
            else -self._absolute_threshold
        )
        accelerations = row["UM_ui_mouseMovements_accelerations"]
        peaks = [
            acc for acc in accelerations if acc > pos_threshold or acc < neg_threshold
        ]

        return peaks

    def _calculate_velocities_and_acceleration(self, movements):
        if (
            is_nan("calculate_velocities_and_acceleration(movements):", movements)
            or None in movements
        ):
            empty_object = {"vel_x": [], "vel_y": [], "acc_x": [], "acc_y": []}
            return empty_object

        vx, vy, ax, ay = [], [], [], []
        dt_velocity = []

        for i in range(1, len(movements)):
            x1, y1, t1 = (
                movements[i - 1]["x"],
                movements[i - 1]["y"],
                movements[i - 1]["timestamp"],
            )
            x2, y2, t2 = movements[i]["x"], movements[i]["y"], movements[i]["timestamp"]

            dx = x2 - x1
            dy = y2 - y1
            dt = (t2 - t1).total_seconds()
            dt_velocity.append(dt)

            vx.append(dx / dt if dt != 0 else 0)
            vy.append(dy / dt if dt != 0 else 0)

        for i in range(1, len(vx)):
            # Adjust index here because dt_velocity is one less than vx, vy
            dt = dt_velocity[i - 1]
            ax.append((vx[i] - vx[i - 1]) / dt if dt != 0 else 0)
            ay.append((vy[i] - vy[i - 1]) / dt if dt != 0 else 0)

        return {"vel_x": vx, "vel_y": vy, "acc_x": ax, "acc_y": ay}

    def _calculate_self_intersections(self, mouse_movements):
        if (
            is_nan("calculate_self_intersections(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        points_seen = set()
        intersection_count = 0

        for point in mouse_movements:
            point_tuple = (point["x"], point["y"])

            if point_tuple in points_seen:
                intersection_count += 1
            points_seen.add(point_tuple)

        return intersection_count

    def _calculate_movement_angles(self, mouse_movements):
        if (
            is_nan("calculate_movement_angles(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        if not mouse_movements or len(mouse_movements) < 2:
            return np.nan

        angles = []
        for i in range(1, len(mouse_movements)):
            x1, y1 = mouse_movements[i - 1]["x"], mouse_movements[i - 1]["y"]
            x2, y2 = mouse_movements[i]["x"], mouse_movements[i]["y"]

            angle = np.arctan2(y2 - y1, x2 - x1)

            angle_degrees = np.degrees(angle)

            angles.append(angle_degrees)

        return angles

    def _calculate_angles_std(self, angles):
        if not angles:
            return np.nan
        return np.std(angles)

    def _calculate_elapsed_time(self, mouse_movements):
        if (
            is_nan("calculate_elapsed_time(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        # if not mouse_movements or len(mouse_movements) == 0:
        if len(mouse_movements) == 0:
            return np.nan

        timestamps = [m["timestamp"] for m in mouse_movements]

        elapsed_time = (max(timestamps) - min(timestamps)).total_seconds()
        return elapsed_time

    def _apply_normalization(self, row):
        viewport = row.get("DFP_js_viewport_inner")
        mouse_movements = row.get("UM_ui_mouseMovements_list")
        if is_nan("DFP_js_viewport_inner", viewport) or is_nan(
            "UM_ui_mouseMovements_list", mouse_movements
        ):
            return None

        orig_width, orig_height = map(int, viewport.split("x"))
        valid_movements = [event for event in mouse_movements if event is not None]
        if not valid_movements:
            return []

        mouse_events = np.array(
            [[event["timestamp"], event["x"], event["y"]] for event in valid_movements]
        )
        return self._normalize_coordinates_origin_type(
            mouse_events, orig_width, orig_height
        )

    def _normalize_coordinates_origin_type(
        self, mouse_events, orig_width, orig_height, target_width=800, target_height=533
    ):
        if mouse_events.size == 0:
            return []

        orig_width = orig_width if orig_width != 0 else target_width
        orig_height = orig_height if orig_height != 0 else target_height

        mouse_events = np.array(mouse_events)

        timestamps = mouse_events[:, 0]
        x_coords = mouse_events[:, 1]
        y_coords = mouse_events[:, 2]

        normalized_x = (x_coords / orig_width) * target_width
        normalized_y = (y_coords / orig_height) * target_height

        normalized_x = np.clip(normalized_x, 0, target_width)
        normalized_y = np.clip(normalized_y, 0, target_height)

        normalized_events = [
            {"timestamp": ts, "x": x, "y": y}
            for ts, x, y in zip(timestamps, normalized_x, normalized_y)
        ]
        return normalized_events

    def _calculate_traveled_distances(self, mouse_movements):
        if (
            is_nan("calculate_traveled_distances(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        if not mouse_movements or len(mouse_movements) < 2:
            return np.nan

        total_distance = 0
        for i in range(len(mouse_movements) - 1):
            x1, y1 = mouse_movements[i]["x"], mouse_movements[i]["y"]
            x2, y2 = mouse_movements[i + 1]["x"], mouse_movements[i + 1]["y"]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            total_distance += distance

        return total_distance

    def _calculate_real_distance(self, mouse_movements):
        if (
            is_nan("calculate_real_distance(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        if len(mouse_movements) < 2:
            return 0
        x1, y1 = mouse_movements[0]["x"], mouse_movements[0]["y"]
        x2, y2 = mouse_movements[-1]["x"], mouse_movements[-1]["y"]
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _calculate_length_ratio(self, mouse_movements):
        if (
            is_nan("calculate_length_ratio(mouse_movements):", mouse_movements)
            or None in mouse_movements
        ):
            return None

        if len(mouse_movements) < 2:
            return np.nan

        curve_length = self._calculate_traveled_distances(mouse_movements)
        real_distance = self._calculate_real_distance(mouse_movements)

        if real_distance == 0:
            return np.nan

        return curve_length / real_distance
