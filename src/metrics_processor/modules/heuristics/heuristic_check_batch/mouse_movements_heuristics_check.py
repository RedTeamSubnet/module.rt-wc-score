import logging
import pandas as pd

from .heuristics_check import HeuristicsCheck


logger = logging.getLogger(__name__)


class MouseMovementsHeursiticsCheck(HeuristicsCheck):
    # _count_threshold = 0
    _max_human_velocity = 18000

    # Define thresholds in constructor
    def __init__(self, max_human_velocity=18000) -> None:
        super().__init__()
        self._max_human_velocity = max_human_velocity

        self._all_heuristic_columns = ['H_bot_ui_mouseMovement_velocity_above_threshold',
                                       'H_bot_UM_ui_mouseMovements_count_veryLow',
                                       'H_bot_UM_ui_mouseMovements_count_low',
                                       'H_bot_UM_ui_mouseMovements_vel_x_std_upper_bound_outlier',
                                       'H_bot_UM_ui_mouseMovements_vel_x_std_lower_bound_outlier',
                                       'H_bot_UM_ui_mouseMovements_vel_x_std_lower_bound_outlier_very_low',
                                       'H_bot_UM_ui_mouseMovements_vel_y_std_upper_bound_outlier',
                                       'H_bot_UM_ui_mouseMovements_vel_y_std_lower_bound_outlier',
                                       'H_bot_UM_ui_mouseMovements_vel_y_std_lower_bound_outlier_very_low',
                                       'H_bot_UM_ui_mouseMovements_self_intersections_zero',
                                       'H_bot_UM_ui_mouseMovements_angles_std_low',
                                       'H_bot_UM_ui_mouseMovements_elapsed_time_low',
                                       'H_bot_UM_ui_mouseMovements_elapsed_time_very_low',
                                       'H_bot_UM_ui_mouseMovements_length_ratio_low',
                                       'H_bot_UM_ui_mouseMovements_length_ratio_one'
                                       ]

    def _check_target_subset(self, target_subset: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame(index=target_subset.index)

        result['H_bot_UM_ui_mouseMovements_count_veryLow'] = target_subset['UM_ui_mouseMovements_count'] <= 2

        result['H_bot_UM_ui_mouseMovements_count_low'] = target_subset['UM_ui_mouseMovements_count'].between(
            3, 10)  # 2 < count <= 10

        #
        result['H_bot_ui_mouseMovement_velocity_above_threshold'] = target_subset['UM_ui_mouseMovements_max_velocity'] > self._max_human_velocity

        result['H_bot_UM_ui_mouseMovements_vel_x_std_upper_bound_outlier'] = target_subset['UM_ui_mouseMovements_vel_x_std'] > 4000

        result['H_bot_UM_ui_mouseMovements_vel_x_std_lower_bound_outlier'] = target_subset['UM_ui_mouseMovements_vel_x_std'].between(
            20, 100)

        result['H_bot_UM_ui_mouseMovements_vel_x_std_lower_bound_outlier_very_low'] = target_subset['UM_ui_mouseMovements_vel_x_std'] < 20

        result['H_bot_UM_ui_mouseMovements_vel_y_std_upper_bound_outlier'] = target_subset['UM_ui_mouseMovements_vel_y_std'] > 3000
        result['H_bot_UM_ui_mouseMovements_vel_y_std_lower_bound_outlier'] = target_subset['UM_ui_mouseMovements_vel_y_std'].between(
            20, 50)

        result['H_bot_UM_ui_mouseMovements_vel_y_std_lower_bound_outlier_very_low'] = target_subset['UM_ui_mouseMovements_vel_y_std'] < 20

        result['H_bot_UM_ui_mouseMovements_self_intersections_zero'] = target_subset['UM_ui_mouseMovements_self_intersections'] == 0

        result['H_bot_UM_ui_mouseMovements_angles_std_low'] = target_subset['UM_ui_mouseMovements_angles_std'] <= 40

        result['H_bot_UM_ui_mouseMovements_elapsed_time_low'] = target_subset['UM_ui_mouseMovements_elapsed_time'].between(
            1.0, 1.5, inclusive='right')

        result['H_bot_UM_ui_mouseMovements_elapsed_time_very_low'] = target_subset['UM_ui_mouseMovements_elapsed_time'].between(
            0, 1, inclusive='right')

        result['H_bot_UM_ui_mouseMovements_length_ratio_low'] = target_subset['UM_ui_mouseMovements_length_ratio'].between(
            1.0, 1.1, inclusive='right')

        result['H_bot_UM_ui_mouseMovements_length_ratio_one'] = target_subset['UM_ui_mouseMovements_length_ratio'] == 1.0

        return result
