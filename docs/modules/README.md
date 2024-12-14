# Modules Configuration

## Overview 

The `Preprocessing` and `Heuristics` modules provide distinct functionalities. Preprocessing receives data, flattens it, and performs feature engineering. Heuristics detects bot-like behavior based on the processed data.

## Processing

### Data Flattening

- **Purpose**: Transform nested JSON metrics into flat structure
- **Input**: Raw metrics data with nested fields (mouse events, keyboard events, checkbox interactions)
- **Output**: Flattened data structure with direct field access

### Feature Engineering

Processes flattened data to extract meaningful features:

- Mouse Events
- Checkbox Interactions

### Mouse Event Analysis

This module identifies bot-like behavior by analyzing:

- Quantity of mouse movements
- Distribution patterns
- Paths between checkbox interactions
- Timing and movement patterns

Analysis types include:

- Velocity Analysis
- Movement Count Analysis

### Scoring

**Individual Scores** - Each analyzer produces a score between 0 and 1:

0.0: Human-like behavior \
1.0: Bot-like behavior

```python
# Example scoring ranges
scores = {
    'highly_suspicious': 0.8 - 1.0,
    'moderately_suspicious': 0.6 - 0.8,
    'slightly_suspicious': 0.4 - 0.6,
    'likely_human': 0.0 - 0.4
}
```

**Weighted Combination** - Combines weights with individual scores

```python
weights = {
    'velocity': 1.0,
    'movement_count': 0.8,
    'checkbox_path': 1.5  # Higher weight as it's more indicative
}
```

**Final Classification** - Threshold for bot detection

- Default threshold: 0.65
- Above threshold: Bot-like
- Below threshold: Human-like

## Sample Input

```json
{
 "project_id": "string",
 "user_id": "string",
 "metrics": {
  "mouse": {
   "movements": [
    {
     "x": "number",
     "y": "number",
     "timestamp": "string"
    }
   ],
   "clicks": [
    {
     "x": "number",
     "y": "number",
     "timestamp": "string",
     "button": "number"
    }
   ],
   "mouseDowns": [
    {
     "x": "number",
     "y": "number",
     "timestamp": "string",
     "button": "number",
     "type": "string"
    }
   ],
   "mouseUps": [
    {
     "x": "number",
     "y": "number",
     "timestamp": "string",
     "button": "number",
     "type": "string"
    }
   ]
  },
  "keyboard": {
   "keypresses": [
    {
     "key": "string",
     "timestamp": "string",
     "modifiers": "string"
    }
   ],
   "keydowns": [
    {
     "key": "string",
     "timestamp": "string",
     "modifiers": "string"
    }
   ],
   "keyups": [
    {
     "key": "string",
     "timestamp": "string",
     "modifiers": "string"
    }
   ],
   "specificKeyEvents": []
  },
  "signInButton": {
   "hoverToClickTime": "number",
   "mouseLeaveCount": "number"
  }
 }
}
```

## Sample Output

```python
{
    'is_bot': 0,  # 0 = human-like, 1 = bot-like
    'confidence': 0.85,
    'score': 0.3,
    'mouse_scores': {
        'velocity': {
            'score': 0.2,
            'weight': 1.0
        },
        'movement_count': {
            'score': 0.4,
            'weight': 0.8
        },
        'checkbox_path': {
            'score': 0.3,
            'weight': 1.5
        }
    },
    'threshold_used': 0.65
}
```

## Configuration

```python
from metrics_processor import MetricsProcessor, MetricsProcessorConfig
from metrics_processor.modules.heuristics import HeuristicConfig
from metrics_processor.modules.preprocessing import PreprocessorConfig

heuristics_configuration = HeuristicConfig(
     mouse_events={
            "velocity": {
                "min_velocity_variation": 200.0,
                "max_velocity_variation": 3000.0,
                "weight": 1.0,
            }
            # ...
    }
)
preprocessor_configuration = PreprocessorConfig(
    feature_engineer={
            "checkbox": {
                "input_field": "checkboxes",
            },
            # ...
    },
     flattener={
            "field_mapping": {
                "project_id": ["project_id"],
                "user_id": ["user_id"],
                "mouse_movements": ["metrics", "mouse", "movements"]
                # ...
            }
     }
)
```

>[!NOTE]
> Full documentation of configuration and explanation for [heuristics](./heuristics/README.md) and [preprocessing](./preprocessing/README.md) modules is available.

## Error Handling

- Input validation (optional)
- Graceful handling of missing data
- Detailed error logging

## Performance

- Minimal CPU usage
- No external API calls
- Real-time analysis capability
- Memory efficient (no state storage)

### Environment Modes

- Development mode: Validation enabled
- Production mode: Validation disabled for optimal performance
