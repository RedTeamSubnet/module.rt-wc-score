import logging
import numpy as np
import pandas as pd

from .feature_engineering import FeatureEngineering


logger = logging.getLogger(__name__)


class MouseDownUpFE(FeatureEngineering):

    def process(self, mouse_down_up_data):
        mousedown_data = mouse_down_up_data.ui_mouseDowns
        mouseup_data = mouse_down_up_data.ui_mouseUps

        if not isinstance(mousedown_data, list):
            mousedown_data = []
        if not isinstance(mouseup_data, list):
            mouseup_data = []

        if not mousedown_data or not mouseup_data:
            total_mousedowns = len(mousedown_data)
            total_mouseups = len(mouseup_data)
            return {
                'ui_mouse_mean_dwell_time': None,
                'ui_mouse_std_dwell_time': None,
                'ui_mouse_mean_inter_click_interval': None,
                'ui_mouse_std_inter_click_interval': None,
                'ui_mouse_total_mousedowns': total_mousedowns,
                'ui_mouse_total_mouseups': total_mouseups,
                'ui_mouse_event_density': None
            }

        min_len = min(len(mousedown_data), len(mouseup_data))

        mousedown_df = pd.DataFrame(mousedown_data[:min_len])
        mouseup_df = pd.DataFrame(mouseup_data[:min_len])

        timestamp_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        mousedown_timestamps = pd.to_datetime(
            mousedown_df['timestamp'], format=timestamp_format)
        mouseup_timestamps = pd.to_datetime(
            mouseup_df['timestamp'], format=timestamp_format)

        dwell_times = mouseup_timestamps - mousedown_timestamps  # timedelta
        dwell_times = dwell_times.dt.total_seconds()

        inter_click_intervals = mousedown_timestamps.diff().shift(-1).dt.total_seconds()  # timedelta

        mean_dwell_time = dwell_times.mean()
        std_dwell_time = dwell_times.std()
        mean_inter_click_interval = inter_click_intervals.mean()
        std_inter_click_interval = inter_click_intervals.std()

        total_mousedowns = len(mousedown_data)
        total_mouseups = len(mouseup_data)

        session_duration = (
            mousedown_timestamps.iloc[-1] - mousedown_timestamps.iloc[0]).total_seconds() if min_len > 1 else 0
        event_density = total_mousedowns / session_duration * \
            60 if session_duration > 0 else None

        return {
            'ui_mouse_mean_dwell_time': mean_dwell_time,
            'ui_mouse_std_dwell_time': std_dwell_time,
            'ui_mouse_mean_inter_click_interval': mean_inter_click_interval,
            'ui_mouse_std_inter_click_interval': std_inter_click_interval,
            'ui_mouse_total_mousedowns': total_mousedowns,
            'ui_mouse_total_mouseups': total_mouseups,
            'ui_mouse_event_density': event_density
        }

