# Heuristics Module

## Overview

The heuristics module analyzes preprocessed features to detect bot-like behavior using various heuristic rules. It provides a scoring system to classify interactions as either human-like or bot-like.

## Key Components

### Mouse Event Analysis

#### 1. Velocity Analysis

- Detects suspicious velocity patterns
- Analyzes movement consistency
- Thresholds:
    - `min_velocity_variation`: 200.0 (too constant if below)
    - `max_velocity_variation`: 3000.0 (too erratic if above)

#### 2. Movement Count Analysis

- Evaluates quantity of movements
- Analyzes distribution patterns
- Thresholds:
    - `min_movement_count`: 15 (suspicious if below)
    - `max_movement_count`: 2000 (suspicious if above)

#### 3. Checkbox Path Analysis

- Analyzes paths between checkbox interactions
- Evaluates timing and movement patterns
- Thresholds:
    - `min_expected_time`: 0.3s (too fast if below)
    - `max_linearity_threshold`: 0.85 (too straight if above)
    - `min_movement_count`: 8 (between checkboxes)

## Scoring System

### Individual Scores

Each analyzer produces a score between 0 and 1:

- 0.0: Human-like behavior
- 1.0: Most bot-like behavior

```python
# Example scoring ranges
scores = {
    'highly_suspicious': 0.8 - 1.0,
    'moderately_suspicious': 0.6 - 0.8,
    'slightly_suspicious': 0.4 - 0.6,
    'likely_human': 0.0 - 0.4
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

- Default threshold: 0.65
- Above threshold: Bot-like
- Below threshold: Human-like

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
    'threshold_used': 0.65
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
config = HeuristicConfig(
    score_threshold=0.55,  # Lower threshold
    mouse_events=MouseEventConfig(
        checkbox_path=CheckboxPathConfig(
            min_expected_time=0.4,  # Require slower interactions
            max_linearity_threshold=0.8  # Less tolerance for straight paths
        )
    )
)
```

#### Lenient Detection

```python
config = HeuristicConfig(
    score_threshold=0.75,  # Higher threshold
    mouse_events=MouseEventConfig(
        checkbox_path=CheckboxPathConfig(
            min_expected_time=0.2,  # Allow faster interactions
            max_linearity_threshold=0.9  # More tolerance for straight paths
        )
    )
)
```

## Performance Impact

- Minimal CPU usage
- No external API calls
- Real-time analysis capability
- Memory efficient (no state storage)
