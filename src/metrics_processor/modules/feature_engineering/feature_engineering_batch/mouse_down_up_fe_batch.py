import logging
import pandas as pd

from .feature_engineering_batch import FeatureEngineeringBatch
from ..feature_engineering import MouseDownUpFE


logger = logging.getLogger(__name__)


class MouseDownUpFEBatch(FeatureEngineeringBatch):
    _feature_handler: MouseDownUpFE

    def __init__(self) -> None:
        super().__init__()
        self._feature_handler = MouseDownUpFE()

    def process(self, mouse_down_up_data: pd.DataFrame):
        # Apply the process method for each row in the DataFrame
        processed_data = mouse_down_up_data.apply(
            self._feature_handler.process, axis=1)

        # Normalize the parsed data into a DataFrame and join with the original DataFrame
        df = pd.json_normalize(processed_data)
        return df
