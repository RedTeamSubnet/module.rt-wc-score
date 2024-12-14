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
from rt_wc_score.modules.preprocessing import Preprocessor

preprocessor = Preprocessor()

features = preprocessor(raw_data)
```

### Example Input/Output

#### Input

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

## Configuration

### Default Configuration

```python
# Checkbox events processing configuration
checkbox_config = {
    "checkbox": {
        "input_field": "checkboxes"  # Field name for checkbox interactions
        }
}
```

```python
# Keyboard events processing configuration
keyboard_config = {
    "keyboard": {
        # Field names for keyboard event data
        "input_field": {
            "keypresses": "keypresses",
            "keydowns": "keydowns",
            "keyups": "keyups",
        },
        "processing": {
            # Names of the output count features
            "feature_names": {
                "keypresses": "keypresses_count",
                "keydowns": "keydowns_count",
                "keyups": "keyups_count",
            },
            # Default value for invalid/missing data
            "default_value": 0.0,
        },
    }
}
```

```python
# Mouse down/up processing configuration
mouse_down_up_config = {
    "mouse_down_up": {
        "down_field": "mouse_mouseDowns",                       # Field name for mouse down events
        "up_field": "mouse_mouseUps",                           # Field name for mouse up events
       # Processing-specific configuration
        "processing": {
            # Names of the output features
            "feature_names": {
                "mouse_downs_total": "mouse_down_total",
                "mouse_ups_total": "mouse_ups_total",
            },
            # Default value for invalid/missing data
            "default_value": 0.0,
        },
    }
}
```

```python
# Mouse movement processing configuration
mouse_movement_config = {
    "mouse_movement": {
        "input_field": "mouse_movements",                                       # Field name for mouse movement data
        
        # Processing-specific configuration
        "processing": {

            "default_factory": {
                "min_movements_required": 2,                                    # Minimum number of movements required to compute velocity
                "fields": {"x": "x", "y": "y", "timestamp": "timestamp"},       # Field names in the movement data
                "velocity_feature_name": "mouse_movement_stddev_velocity",      # Name of the output velocity feature
                "movements_count_feature_name": "mouse_movement_count",         # Name of the output mouse movement count feature
            }
        }
    }
}
```

```python
# Data Flattening Field Mapping
field_mapping = {
    "project_id": ["project_id"],
    "user_id": ["user_id"],
    "mouse_movements": ["metrics", "mouse", "movements"],
    "mouse_clicks": ["metrics", "mouse", "clicks"],
    "mouse_mouseDowns": ["metrics", "mouse", "mouseDowns"],
    "mouse_mouseUps": ["metrics", "mouse", "mouseUps"],
    "keypresses": ["metrics", "keyboard", "keypresses"],
    "keydowns": ["metrics", "keyboard", "keydowns"],
    "keyups": ["metrics", "keyboard", "keyups"],
    "keyboard_specificKeyEvents": ["metrics", "keyboard", "specificKeyEvents"],
    "signInButton_hoverToClickTime": ["metrics", "signInButton", "hoverToClickTime"],
    "signInButton_mouseLeaveCount": ["metrics", "signInButton", "mouseLeaveCount"],
    "checkboxes": ["additional", "checkbox_interactions"],
}
```

```python
#  Input data for JSON flattening
input_data_template = {
    "metrics": {
        #  Mouse metrics data.
        "mouse": {
            "movements": [], "clicks": [],
            "mouseDowns": [], "mouseUps": []
        },
        # Keyboard metrics data.
        "keyboard": {
            "keypresses": [], "keydowns": [],
            "keyups": [], "specificKeyEvents": []
        },
        # Sign-in button metrics data.
        "signInButton": {
            "hoverToClickTime": None,
            "mouseLeaveCount": 0
        }
    },
    "additional": None,
    "project_id": None,
    "user_id": None
}
```

```python
#Main configuration for feature engineering
feature_engineer_config = {
    **checkbox_config,
    **keyboard_config,
    **mouse_down_up_config,
    **mouse_movement_config
}
```

```python
# Configuration for JSON data flattening.
flattener_config = {
    "field_mapping": field_mapping,
    "input_data": input_data_template,
    "is_validate":False
}
```

```python
config = PreprocessorConfig(
    feature_engineer=feature_engineer_config,    # Configuration for feature engineering
    flattener=flattener_config                   #Configuration for JSON flattening
)
```

>[Note]
> You can change anything according to your input data.

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

## Error Handling

- Input validation (optional)
- Graceful handling of missing data
- Detailed error logging

## Performance Considerations

- Development mode: Validation enabled
- Production mode: Validation disabled for better performance
