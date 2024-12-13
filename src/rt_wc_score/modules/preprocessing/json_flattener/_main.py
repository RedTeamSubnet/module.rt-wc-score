"""Module for flattening nested JSON data structures."""

import json
import logging
from typing import Dict, List, Optional, Union, Any
from functools import reduce
from operator import getitem

from pydantic import ValidationError
from .._base import BasePreprocessor
from .config import JsonDataFlattenerConfigPM

logger = logging.getLogger(__name__)


class JsonDataFlattener(BasePreprocessor):
    """Preprocessor for flattening nested JSON data."""

    def __init__(self, config: Optional[JsonDataFlattenerConfigPM] = None) -> None:
        super().__init__()
        self._flattened_data: Optional[Dict[str, Any]] = None
        self.config = config or JsonDataFlattenerConfigPM()

    def _get_nested_value(
        self, data: Dict[str, Any], path: List[str], field_name: str
    ) -> Any:
        """Get value from nested dictionary using path."""
        logger.debug(f"Getting value for {field_name} using path {path}")
        try:
            current = data
            for key in path:
                current = current[key]
            return current
        except (KeyError, TypeError) as e:
            logger.debug(f"Failed to get value for {field_name}: {str(e)}")
            return []

    def _extract_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and flatten metrics from the data dictionary."""
        try:
            flattened = {}
            for field_name, path in self.config.field_mapping.items():
                try:
                    value = self._get_nested_value(data, path, field_name)
                    flattened[field_name] = value
                    logger.debug(f"Successfully extracted {field_name}")
                except Exception as e:
                    logger.error(f"Error extracting {field_name}: {str(e)}")
                    raise
            return flattened
        except Exception as e:
            logger.error(f"Error in _extract_metrics: {str(e)}")
            raise

    def __call__(self, data: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Process input data and return flattened structure."""
        try:
            if isinstance(data, str):
                data = json.loads(data)
                logger.debug("Successfully parsed JSON string")

            if self.config.is_validate:
                parsed_data = self.config.input_data.model_validate(data).model_dump()
                logger.debug("Successfully validated input data")
            else:
                parsed_data = data

            logger.debug("Starting metrics extraction")
            self._flattened_data = self._extract_metrics(parsed_data)
            return self._flattened_data

        except Exception as e:
            logger.error(f"Error during flattening: {str(e)}")
            return None
