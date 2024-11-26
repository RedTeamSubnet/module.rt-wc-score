import logging

import pandas as pd
from ..preprocessing.feature_preproccessor import PreProccessData

from .feature_engineering_batch import (
    MouseMovementFEBatch,
    MouseDownUpFEBatch,
    MouseMovementsHComputationBatch,
)


logger = logging.getLogger(__name__)
class SSFeatureEnginnering:
    """Base class to processing features from given datafrom.

    Attributes:
        raw_df (pd.DataFrame): Input data for feature engineering.

    Methods:
        run (): Runs class to get resultent dataframe.
     """

    _input_df: pd.DataFrame = None

    def run(self, raw_df: pd.DataFrame) -> pd.DateOffset:
        """Base function to run and get resultant dataframe

        Attributes:
            raw_df (pd.DataFrame): Input data for feature engineering

        Returns:
            DataFrame: resultant data after feature engineering
        """

        self._navigator_prefix = 'nav'
        self._dedicated_worker_prefix = 'dw'
        self._shared_worker_prefix = 'sw'
        self._header_data_prefix = 'hdr_ua'

        self._input_df = raw_df

        parser = PreProccessData()
        self._input_df = parser.parse(raw_df)

        mouse_df = MouseMovementFEBatch().process(
            self._input_df['ui_mouseMovements_list'])
        # Extract mouse down/up events data
        mouse_down_up_df = MouseDownUpFEBatch().process(
            self._input_df[['ui_mouseDowns', 'ui_mouseUps']]
        )


        # concat all extracted features
        self._input_df = pd.concat(
            [
                self._input_df,
                mouse_df,
                mouse_down_up_df,

            ],
            axis=1,
        )
        # Extracting touch informations
        touch_events_h_df = MouseMovementsHComputationBatch().process(self._input_df)
        self._input_df = pd.concat(
            [
                self._input_df,
                touch_events_h_df,  # adding extra features
            ],
            axis=1,
        )
        return self._input_df
