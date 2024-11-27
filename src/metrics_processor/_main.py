"""Main module for processing metrics data through preprocessing and heuristics."""

import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from .modules.preprocessing import Preprocessor, PreprocessorConfig
from .modules.heuristics import HeuristicAnalyzer, HeuristicConfig

logger = logging.getLogger(__name__)


class MetricsProcessorConfig(BaseModel):
    """Configuration for metrics processing pipeline."""

    preprocessor: PreprocessorConfig = Field(
        default_factory=PreprocessorConfig,
        description="Configuration for preprocessing",
    )
    heuristics: HeuristicConfig = Field(
        default_factory=HeuristicConfig,
        description="Configuration for heuristic analysis",
    )

    class Config:
        frozen = True


class MetricsProcessor:
    """Main class for processing metrics data through preprocessing and heuristic analysis."""

    def __init__(self, config: Optional[MetricsProcessorConfig] = None):
        """Initialize the metrics processor pipeline.

        Args:
            config: Configuration for the processing pipeline
        """
        self.config = config or MetricsProcessorConfig()

        self.preprocessor = Preprocessor(config=self.config.preprocessor)
        self.heuristic_analyzer = HeuristicAnalyzer(config=self.config.heuristics)

    def __call__(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw metrics data through the pipeline.

        Args:
            raw_data: Raw metrics data

        Returns:
            Dictionary containing preprocessed features and analysis results
        """
        try:
            # Step 1: Preprocess the data
            logger.info("Preprocessing raw data...")
            processed_features = self.preprocessor(raw_data)

            if processed_features is None:
                logger.error("Preprocessing failed")
                return {
                    "success": False,
                    "error": "Preprocessing failed",
                    "stage": "preprocessing",
                }

            # Step 2: Run heuristic analysis
            logger.info("Running heuristic analysis...")
            analysis_results = self.heuristic_analyzer(processed_features)

            return {
                "success": True,
                "features": processed_features,
                "analysis": analysis_results,
            }

        except Exception as e:
            logger.error(f"Error in metrics processing: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e), "stage": "processing"}
