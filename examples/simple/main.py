#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import logging
from pathlib import Path

from rt_wc_score.modules.preprocessing import Preprocessor

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    _data_dir_path = Path(__file__).parent.parent.parent / "data"
    _raw_json_data_path = _data_dir_path / "raw" / "raw.json"
    _processed_json_data_path = _data_dir_path / "processed" / "processed.json"

    _raw_json_data_path.parent.mkdir(parents=True, exist_ok=True)
    _processed_json_data_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Reading data from: {_raw_json_data_path}")
    try:
        with open(_raw_json_data_path, "r") as f:
            raw_data = f.read()
            json_data = json.loads(raw_data)
            logger.debug(
                f"Raw data structure: {json.dumps(json_data, indent=2)[:500]}..."
            )
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in input file: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error(f"Input file not found: {_raw_json_data_path}")
        sys.exit(1)

    logger.info("Initializing preprocessor...")
    preprocessor = Preprocessor()

    logger.info("Processing data...")
    processed_data = preprocessor(raw_data)

    if processed_data is None:
        logger.error("Failed to process data")
        sys.exit(1)

    logger.info(f"Writing processed data to: {_processed_json_data_path}")
    with open(_processed_json_data_path, "w") as f:
        json.dump(processed_data, f, indent=2)

    logger.info("Done!")
