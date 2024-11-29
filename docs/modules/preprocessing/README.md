# Preprocessing Module

## Overview

The preprocessing module transforms raw interaction metrics into analyzable features through a two-stage pipeline consisting of data flattening and feature engineering.

## Key Components

### 1. Data Flattening

- **Purpose**: Transform nested JSON metrics into flat structure
- **Input**: Raw metrics data with nested fields (mouse events, keyboard events, checkbox interactions)
- **Output**: Flattened data structure with direct field access

### 2. Feature Engineering

Processes flattened data to extract meaningful features:

#### Mouse Events

- Velocity analysis
- Movement counts
- Pattern detection

#### Checkbox Interactions

- Click timing analysis
- Path analysis between checkboxes
- Movement patterns

## Usage

### Basic Usage

```python
from metrics_processor.modules.preprocessing import Preprocessor

preprocessor = Preprocessor()

features = preprocessor(raw_data)
```

### Example Input/Output

#### Input

```json
{
    "project_id": "app-123",
    "metrics": {
        "mouse": {
            "movements": [...],
            "mouseDowns": [...]
        },
        "additional": {
            "checkbox_interactions": [...]
        }
    }
}
```

#### Output Features

```python
{
    "mouse_movement_stddev_velocity": 1775.83,
    "mouse_movement_count": 106,
    "checkbox_1_2_time_diff": 1.5,
    "checkbox_1_2_path_linearity": 0.85
    # ... other features
}
```

## Configuration

### Main Configuration Options

```python
config = PreprocessorConfig(
    is_validate=True,  # enable/disable validation
    field_mapping={    # custom field mapping
        "movements": ["metrics", "mouse", "movements"],
        # ... other mappings
    }
)
```

## Error Handling

- Input validation (optional)
- Graceful handling of missing data
- Detailed error logging

## Performance Considerations

- Development mode: Validation enabled
- Production mode: Validation disabled for better performance
