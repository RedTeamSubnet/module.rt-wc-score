# Project Structure

## Directory Structure

```bash
rt_wc_score/
├── __init__.py
├── _main.py           # Main MetricsProcessor class
├── config.py          # Top-level configuration
├── modules/
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── json_flattener/
│   │   │   ├── __init__.py
│   │   │   ├── _main.py
│   │   │   └── config.py
│   │   └── feature_engineering/
│   │       ├── __init__.py
│   │       ├── _main.py
│   │       ├── config.py
│   │       ├── mouse_events/
│   │       ├── keyboard_events/
│   │       └── checkbox_events/
│   └── heuristics/
│       ├── __init__.py
│       ├── _main.py
│       ├── config.py
│       └── mouse_events/
│           ├── velocity/
│           ├── movement_count/
│           └── checkbox_path/
```

## Module Overview

### 1. MetricsProcessor (Top Level)

```python
from metrics_processor import MetricsProcessor

processor = MetricsProcessor()
results = processor(raw_data)
```

- Main entry point for processing
- Coordinates preprocessing and heuristics
- Handles overall configuration

### 2. Preprocessing Module

#### JSON Flattener

- Transforms nested input data
- Handles field mapping
- Validates data structure

#### Feature Engineering

- Mouse movement processing
- Keyboard event processing
- Checkbox interaction analysis

### 3. Heuristics Module

- Mouse event analysis
- Bot detection algorithms
- Score calculation and classification

## Data Flow

1. Raw Input → JSON Flattener
2. Flattened Data → Feature Engineering
3. Features → Heuristic Analysis
4. Analysis → Final Results

## Configuration Hierarchy

```bash
MetricsProcessorConfig
├── PreprocessorConfig
│   ├── JsonDataFlattenerConfig
│   └── FeatureEngineerConfig
└── HeuristicConfig
    └── MouseEventConfig
```
