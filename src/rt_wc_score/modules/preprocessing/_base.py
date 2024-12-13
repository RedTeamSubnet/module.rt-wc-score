import logging
from typing import Any
from abc import ABC, abstractmethod


logger = logging.getLogger(__name__)


class BasePreprocessor(ABC):
    """Abstract base class for data preprocessing."""

    @abstractmethod
    def __call__(self, data: Any) -> Any:
        """Process the input data."""
        pass
