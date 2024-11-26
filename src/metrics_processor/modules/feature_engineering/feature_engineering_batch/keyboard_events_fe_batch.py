import logging
import pandas as pd

from .feature_engineering_batch import FeatureEngineeringBatch
from ..feature_engineering import KeyboardEventsFE


logger = logging.getLogger(__name__)


class KeypressEventsFEBatch(FeatureEngineeringBatch):
    _feature_handler: KeyboardEventsFE

    def __init__(self) -> None:
        super().__init__()
        self._feature_handler = KeyboardEventsFE()

    def process(self, compute_keyboards: pd.DataFrame):
        processed_data = compute_keyboards.apply(
            self._feature_handler.process, axis=1)

        # Normalize the parsed data into a DataFrame and join with the original DataFrame
        df = pd.json_normalize(processed_data)
        return df

