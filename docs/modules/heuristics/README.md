# Heuristics Module

## Overview

The heuristics module analyzes preprocessed features to detect bot-like behavior using various heuristic rules. It provides a scoring system to classify interactions as either human-like or bot-like.

## Key Components

### Mouse Event Analysis

#### 1. Velocity Analysis

- Detects suspicious velocity patterns
- Analyzes movement consistency
- Thresholds:
    - `min_velocity_variation`: 1000.0 (too constant if below)
    - `max_velocity_variation`: 2500.0 (too erratic if above)

#### 2. Movement Count Analysis

- Evaluates quantity of movements
- Analyzes distribution patterns
- Thresholds:
    - `min_movement_count`: 100 (suspicious if below)
    - `max_movement_count`: 700 (suspicious if above)

#### 3. Checkbox Path Analysis

- Analyzes paths between checkbox interactions
- Evaluates timing and movement patterns
- Thresholds:
    - `min_expected_time`: 1s (too fast if below)
    - `max_linearity_threshold`: 0.95 (too straight if above)
    - `min_movement_count`: 20 (between checkboxes)

## Scoring System

### Individual Scores

Each analyzer produces a score between 0 and 1:

- 1.0: Human-like behavior
- 0.0: Most bot-like behavior

```python
# Example scoring ranges
scores = {
    'highly_suspicious': 0.0 - 2.0,
    'moderately_suspicious': 0.4 - 0.6,
    'slightly_suspicious': 0.6 - 0.8,
    'likely_human': 0.8 - 1.0
}
```

### Weighted Combination

```python
weights = {
    'velocity': 1.0,
    'movement_count': 0.8,
    'checkbox_path': 1.5  # Higher weight as it's more indicative
}
```

### Final Classification

- Default threshold: 0.35
- Above threshold: Human-like
- Below threshold: Bot-like

## Usage

### Basic Usage

```python
from metrics_processor.modules.heuristics import HeuristicAnalyzer

# Initialize
analyzer = HeuristicAnalyzer()

# Analyze features
results = analyzer(features)
```

### Example Output

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
    'threshold_used': 0.35
}
```

## Configuration

### Adjusting Sensitivity

```python
config = HeuristicConfig(
    score_threshold=0.65,  # Classification threshold
    mouse_events=MouseEventConfig(
        velocity=VelocityConfig(
            min_velocity_variation=200.0,
            max_velocity_variation=3000.0,
            weight=1.0
        ),
        checkbox_path=CheckboxPathConfig(
            min_expected_time=0.3,
            max_linearity_threshold=0.85,
            weight=1.5
        )
    )
)
```

### Common Configurations

#### Strict Detection

```python
HeuristicConfig(
    mouse_events={
        "velocity": {
            "min_velocity_variation":       1000.0,  # Minimum expected velocity standard deviation
            "max_velocity_variation":       2500.0,  # Maximum expected velocity standard deviation
            "weight":                       1.0,     # Weight for velocity analysis
        },
        "movement_count": {
            "min_movement_count":           100,     # Minimum expected mouse movements
            "max_movement_count":           700,     # Maximum expected mouse movements
            "min_movement_count_too_low":   5,       # Minimum mouse movement count to consider user as bot
            "weight":                       0.8,     # Weight for movement count analysis
        },
        "checkbox_path": {
            "min_expected_time":            1,       # Minimum expected time between checkbox clicks (seconds)
            "max_expected_time":            5,       # Maximum expected time between checkbox clicks (seconds)
            "min_linearity_threshold":      0.75,    # Threshold for suspiciously linear paths
            "max_linearity_threshold":      0.95,    # Threshold for suspiciously linear paths
            "min_movement_count":           20       # Minimum expected movements between checkboxes
            "min_movement_count_too_low":   3        # Minimum expected movements between checkboxes
            "max_avg_angle_degrees":        0.40,    # Max average angle between movements
            "min_avg_angle_degrees":        0.05,    # Min average angle between movements
            "weight":                       1.5      # Weight for checkbox path analysis
        },
    },
    "score_threshold":                      0.65,    # Threshold for bot classification (>threshold = bot)
)
```

## Performance Impact

- Minimal CPU usage
- No external API calls
- Real-time analysis capability
- Memory efficient (no state storage)
