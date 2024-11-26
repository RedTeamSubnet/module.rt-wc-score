import logging
import pandas as pd

from .feature_engineering_batch import FeatureEngineeringBatch
from ..feature_engineering import MouseMovementFE


logger = logging.getLogger(__name__)


class MouseMovementFEBatch(FeatureEngineeringBatch):
    _feature_handler: MouseMovementFE

    def __init__(self) -> None:
        super().__init__()
        self._feature_handler = MouseMovementFE()

    def process(self, mouse_movements_data: pd.Series):
        processed_data = mouse_movements_data.apply(
            self._feature_handler.process)

        df = pd.json_normalize(processed_data)
        return df
