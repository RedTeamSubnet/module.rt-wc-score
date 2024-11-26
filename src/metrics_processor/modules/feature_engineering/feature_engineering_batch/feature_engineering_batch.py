import pandas as pd
from abc import ABC, abstractmethod

from ..feature_engineering import FeatureEngineering


class FeatureEngineeringBatch(ABC):
    _input_data: pd.DataFrame
    _feature_handler: FeatureEngineering

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    # @abstractmethod
    # def perform_computation(self, df: pd.DataFrame) -> pd.Series:
    #     """Perform the heuristic computation on the DataFrame and return a Series with the results."""
    #     pass
