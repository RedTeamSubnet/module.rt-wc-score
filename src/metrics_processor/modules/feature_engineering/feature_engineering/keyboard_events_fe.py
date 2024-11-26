import logging
import numpy as np

from .feature_engineering import FeatureEngineering 


logger = logging.getLogger(__name__)


class KeyboardEventsFE(FeatureEngineering):

    def process(self, events: dict):
        keypress_count = np.nan
        keydown_count = np.nan
        keyup_count = np.nan

        if isinstance(events['ui_keypresses'], list):
            keypress_count = len(events['ui_keypresses'])
        if isinstance(events['ui_keydowns'], list):
            keydown_count = len(events['ui_keydowns'])
        if isinstance(events['ui_keyups'], list):
            keyup_count = len(events['ui_keyups'])

        result = {
            'ui_keypresses_count': keypress_count,
            'ui_keydowns_count': keydown_count,
            'ui_keyups_count': keyup_count
        }

        return result
