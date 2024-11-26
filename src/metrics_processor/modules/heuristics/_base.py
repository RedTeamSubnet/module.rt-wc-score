import logging

import pandas as pd
from .heuristic_check_batch import (
    MouseMovementsHeursiticsCheck,
)
from ss_dynamic_ui_set.utils import Retriever


logger = logging.getLogger(__name__)


class SSHeuristicsManager:
    """Base class for heuristic checks. All heuristics checked here and concatenated into single dataframe.

    Attributes:
        _input_df (pd.DataFrame):  Data after for checking heuristics.

    Methods:
        run (): Runs class to check heuristics.
    """

    _input_df: pd.DataFrame = None

    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Base fucntion for heuristic checks. All heuristics checked here and concatenated into single dataframe.

        Attributes:
            df (pd.DataFrame):  Dataframe for checking heuristics.

        Returns:
            DataFrame: Combines the outcomes of heuristic checks with the supplied data.
        """
        self._input_df = df

        device_classification = DeviceClassifier.preprocess_and_classify(self._input_df)
        self._input_df = pd.concat([self._input_df, device_classification], axis=1)

        heuristics_df = self._run_all_heuristic_checks()
        # final_df = HeuristicsBotnessScoreMaker().make_score(heuristics_df)

        # return final_df
        return heuristics_df

    def _run_all_heuristic_checks(self):
        retriever = Retriever(data=self._input_df)
        self._input_df["DFP_nav_client_hints_br"] = retriever.retrieve(
            "DFP_nav_client_hints_br"
        )
        desktop_mask = self._input_df["is_desktop"]
        mobile_mask = ~desktop_mask
        brave_browser_mask = self._input_df["DFP_nav_client_hints_br"].isin(["Brave"])
        no_brave_browser_mask = ~brave_browser_mask
        no_ios_mask = (
            ~self._input_df["DFP_nav_os_family"]
            .fillna("")
            .str.contains("iOS|iPhone|Mac OS", case=False, na=True)
        )
        mobile_and_no_ios_mask_and_no_brave = (
            mobile_mask & no_ios_mask & no_brave_browser_mask
        )

        # version_mask = df['meta_version'] == '1.2.6'
        # combined_mask = desktop_mask & version_mask

        window_resize_heur_df = WindowResizeHeursiticsCheck().check(
            self._input_df["UM_ui_windowResizes"], desktop_mask
        )

        # screen_size_heur_df = self._check_screen_size_heuristics()

        mouse_movements_heur_df = self._check_mouse_movements_heuristics(desktop_mask)

        # device_orient_heur_df = DeviceOrientationEventsHeursiticsCheck().check(
        #     self._input_df["UM_ui_deviceOrientationEvents_count"],
        #     mask=mobile_and_no_ios_mask_and_no_brave,
        # )

        # device_motion_heur_df = DeviceMotionEventsHeursiticsCheck().check(
        #     # ui_deviceMotionEvents_co
        #     self._input_df["UM_ui_deviceMotionEvents_count"],
        #     mask=mobile_and_no_ios_mask_and_no_brave,
        # )

        # touch_events_heur_df = self._check_touch_events_heuristics(mobile_mask)

        # Concatenate all computed/checked DataFrames in one operation

        final_df = pd.concat(
            [
                self._input_df,
                window_resize_heur_df,
                # screen_size_heur_df,
                mouse_movements_heur_df,
                # device_orient_heur_df,
                # device_motion_heur_df,
                # touch_events_heur_df,
            ],
            axis=1,
        )

        pre_op_cols = final_df.columns

        # all the _heur_df dataframes create index column named 0 as a side-effect, let's drop that col
        if 0 in final_df.columns:
            final_df.drop(columns=[0], axis=1, inplace=True)

        after_op_cols = final_df.columns

        return final_df

    # def _check_screen_size_heuristics(self):

    #     screen_heur_computation_result = self._input_df
    #     # let's add columns that are used in ScreenSizeHeursiticsCheck
    #     screen_heur_computation_result[
    #         ["DFP_js_scr_devicePixelRatio", "DFP_dw_br_family"]
    #     ] = self._input_df[["DFP_js_scr_devicePixelRatio", "DFP_dw_br_family"]].copy()

    #     screen_size_heur_checks_df = ScreenSizeHeursiticsCheck().check(
    #         self._input_df
    #     )

    #     # Return only newly created columns
    #     new_cols = [
    #         col
    #         for col in screen_size_heur_checks_df.columns
    #         if col not in self._input_df.columns
    #     ]

    #     return screen_size_heur_checks_df[new_cols]

    def _check_mouse_movements_heuristics(self, mask):

        mouse_movements_df = MouseMovementsHeursiticsCheck().check(
            self._input_df[
                [
                    "UM_ui_mouseMovements_count",
                    "UM_ui_mouseMovements_vel_x_std",
                    "UM_ui_mouseMovements_vel_y_std",
                    "UM_ui_mouseMovements_self_intersections",
                    "UM_ui_mouseMovements_angles_std",
                    "UM_ui_mouseMovements_elapsed_time",
                    "UM_ui_mouseMovements_length_ratio",
                    "UM_ui_mouseMovements_max_velocity",
                ]
            ],
            mask=mask,
        )

        return pd.concat([mouse_movements_df, mouse_movements_df], axis=1)

    def _check_touch_events_heuristics(self, mask):

        touch_events_checks_df = TouchEventsHeursiticsCheck().check(
            self._input_df[
                [
                    "UM_ui_touch_count",
                    "UM_ui_touch_average_speed",
                    "UM_ui_touch_std_speed",
                    "UM_ui_touch_max_speed",
                    "UM_ui_touch_min_speed",
                    "UM_ui_touch_average_acceleration",
                    "UM_ui_touch_std_acceleration",
                    "UM_ui_touch_max_acceleration",
                    "UM_ui_touch_min_acceleration",
                    "UM_ui_touch_speeds",
                    "UM_ui_touch_accelerations",
                ]
            ],
            mask,
        )

        return touch_events_checks_df
