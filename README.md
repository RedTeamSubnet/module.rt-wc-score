# RedTeam Scoring

A Python package for processing and analyzing user interaction metrics to detect bot-like behavior. The package processes raw interaction data (mouse movements, keyboard events, checkbox interactions) and provides both feature extraction and bot detection capabilities.

## 🚀 Installation

### ⚙️ Prerequisites

- Python 3.10+
- pip

### 🛠️ Environment Setup

#### Using Conda

```bash
# Create conda environment
conda create -n metrics-process python=3.11
conda activate metrics-process
```

#### Using venv

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Unix/macOS
# OR
.\venv\Scripts\activate  # On Windows
```

### 📦 Repository Setup

1. Clone the repository using either SSH or HTTPS:

```bash
# Using SSH
git clone git@github.com:InnerWorks-me/module.rt-scoring.git

# OR using HTTPS
git clone https://github.com/InnerWorks-me/module.rt-scoring.git

cd module.rt-scoring
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## ⚡ Quick Start

```python
from metrics_processor import MetricsProcessor

processor = MetricsProcessor()

raw_data = {
    "project_id": "your-app-id",
    "user_id": "user123",
    "metrics": {
        "mouse": {
            "movements": [
                {
                    "x": 745,
                    "y": 155,
                    "timestamp": "2024-11-27T00:19:48.380Z"
                }
                # ... more movements
            ],
            "mouseDowns": [],
            "mouseUps": []
        },
        "keyboard": {
            "keypresses": [],
            "keydowns": [],
            "keyups": []
        }
    },
    "additional": {
        "checkbox_interactions": [
            {
                "checkboxId": 1,
                "x": 25,
                "y": 19,
                "timestamp": "2024-11-28T02:40:12.458Z",
                "checked": true
            }
        ]
    }
}

results = processor(raw_data)
```

## 📚 Documentation

Detailed documentation is available in the [docs](docs) directory:

### 📖 Core Documentation

- [Documentation Guide](docs/README.md) - Start here
- [Project Structure](docs/structure.md) - Code organization and architecture

### 🔍 Module Documentation

- [Preprocessing Module](docs/modules/preprocessing/README.md)
    - Data transformation
    - Feature engineering
    - Event processing

- [Heuristics Module](docs/modules/heuristics/README.md)
    - Bot detection algorithms
    - Scoring system
    - Configuration options

## 💡 Usage Examples

### Basic Usage

```python
processor = MetricsProcessor()

results = processor(raw_data)

if results['success']:
    is_bot = results['analysis']['is_bot']
    confidence = results['analysis']['confidence']
    print(f"Bot Detection: {'🤖' if is_bot else '👤'}")
    print(f"Confidence: {confidence:.2f}")
else:
    print(f"Processing failed: {results['error']}")
```

### Custom Configuration

```python
from metrics_processor import MetricsProcessorConfig
from metrics_processor.modules.heuristics import HeuristicConfig

# Configure with custom settings
config = MetricsProcessorConfig(
    heuristics=HeuristicConfig(
        score_threshold=0.65  # Adjust bot detection threshold
    )
)

processor = MetricsProcessor(config=config)
```

## 📊 Output Format

```python
{
    'success': True,
    'features': {
        'mouse_movement_stddev_velocity': 1775.83,
        'mouse_movement_count': 106,
        'checkbox_1_2_time_diff': 1.5,
        'checkbox_1_2_path_linearity': 0.85,
        # ... more features
    },
    'analysis': {
        'is_bot': 0,  # 0 = human-like, 1 = bot-like
        'confidence': 0.85,
        'score': 0.3,
        'mouse_scores': {
            'velocity': {'score': 0.2, 'weight': 1.0},
            'movement_count': {'score': 0.4, 'weight': 0.8},
            'checkbox_path': {'score': 0.3, 'weight': 1.5}
        },
        'threshold_used': 0.65
    }
}
```

## ⚠️ Error Handling

```python
try:
    results = processor(raw_data)
    if not results['success']:
        print(f"❌ Processing failed: {results['error']}")
        print(f"❌ Failed at stage: {results['stage']}")
except Exception as e:
    print(f"❌ Error: {str(e)}")
```

## 👨‍💻 Development

### Code Style

This project uses:

- ✨ Black for code formatting

```bash
black .
```

## License
