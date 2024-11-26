import logging
import numpy as np

from .feature_engineering import FeatureEngineering


logger = logging.getLogger(__name__)


class MouseMovementFE(FeatureEngineering):

    def process(self, mouse_movement_data):
        mouse_calcs = self.compute_mouse_metrics(mouse_movement_data)

        # mouse velocity and acceleration
        velocities, accel = mouse_calcs

        result = {
            'ui_mouseMovements_accelerations': accel,

            'ui_mouseMovements_min_velocity': np.nan,
            'ui_mouseMovements_max_velocity': np.nan,
            'ui_mouseMovements_mean_velocity': np.nan,
            'ui_mouseMovements_stddev_velocity': np.nan,
            'ui_mouseMovements_var_velocity': np.nan,

            'ui_mouseMovements_min_acceleration': np.nan,
            'ui_mouseMovements_max_acceleration': np.nan,
            'ui_mouseMovements_mean_acceleration': np.nan,
            'ui_mouseMovements_stddev_acceleration': np.nan,
            'ui_mouseMovements_var_acceleration': np.nan

        }

        if velocities:
            result['ui_mouseMovements_min_velocity'] = np.min(velocities)
            result['ui_mouseMovements_max_velocity'] = np.max(velocities)
            result['ui_mouseMovements_mean_velocity'] = np.mean(velocities)
            result['ui_mouseMovements_stddev_velocity'] = np.std(velocities)
            result['ui_mouseMovements_var_velocity'] = np.var(velocities)

        if accel:
            result['ui_mouseMovements_min_acceleration'] = np.min(accel)
            result['ui_mouseMovements_max_acceleration'] = np.max(accel)
            result['ui_mouseMovements_mean_acceleration'] = np.mean(accel)
            result['ui_mouseMovements_stddev_acceleration'] = np.std(accel)
            result['ui_mouseMovements_var_acceleration'] = np.var(accel)

        return result

    def compute_mouse_metrics(self, mouse_movements):
        velocities = []
        accelerations = []

        if not mouse_movements:
            return [], []

        x_coords = np.array([m.get('x')
                            for m in mouse_movements if m is not None])
        y_coords = np.array([m.get('y')
                            for m in mouse_movements if m is not None])
        timestamps = np.array([m.get('timestamp').timestamp()
                              for m in mouse_movements if m is not None])

        if len(x_coords) < 2 or len(y_coords) < 2 or len(timestamps) < 2:
            return [], []

        dx = np.diff(x_coords)
        dy = np.diff(y_coords)
        dt = np.diff(timestamps)

        distances = np.sqrt(dx**2 + dy**2)
        velocities = np.divide(
            distances, dt, out=np.zeros_like(distances), where=dt != 0)

        if len(velocities) > 1:
            d_velocities = np.diff(velocities)
            accelerations = np.divide(d_velocities, dt[1:], out=np.zeros_like(
                d_velocities), where=dt[1:] != 0)
        else:
            accelerations = np.array([])

        return velocities.tolist(), accelerations.tolist()
