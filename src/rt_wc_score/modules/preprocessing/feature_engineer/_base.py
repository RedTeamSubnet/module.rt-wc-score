import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any

import numpy as np


class BaseFeatureEngineer(ABC):
    """Abstract base class for feature engineering processors."""

    @abstractmethod
    def __call__(self, data: Any) -> Dict[str, Any]:
        """Process the input data and return computed features."""
        pass
