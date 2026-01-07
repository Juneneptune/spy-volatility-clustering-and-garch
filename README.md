# SPY Volatility Clustering and GARCH

A Python project for analyzing volatility clustering in SPY (S&P 500 ETF) data and implementing GARCH models for volatility forecasting.

## Project Structure

```
spy-volatility-clustering-and-garch/
├── configs/                    # Configuration files
│   └── default.yaml           # Default configuration for data loading and model parameters
│
├── data/                       # Data storage directory (created at runtime)
│   └── spy/                   # SPY price data storage
│       └── spy_prices.csv     # Downloaded SPY historical prices (auto-generated)
│
├── datasets/                   # Additional datasets (if any)
│
├── notebooks/                  # Jupyter notebooks for analysis
│   └── volatility_basics.ipynb
│
├── scripts/                    # Utility scripts
│   └── test_load_spy.py       # Script to test SPY data loading
│
├── src/                        # Source code
│   └── spy_volatility/        # Main package
│       ├── __init__.py
│       ├── data/              # Data loading and processing modules
│       │   ├── __init__.py
│       │   └── loaders.py    # SPY data download and loading utilities
│       ├── models/            # GARCH and volatility models
│       │   ├── __init__.py
│       │   └── garch_models.py  # GARCH model implementations
│       ├── training/          # Model training utilities
│       │   └── __init__.py
│       └── utils/             # Utility functions
│           ├── __init__.py
│           └── config.py     # Configuration loading utilities
│
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup configuration
└── README.md                  # This file
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spy-volatility-clustering-and-garch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Dependencies

The project requires the following Python packages:
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Plotting
- `yfinance` - Yahoo Finance data download
- `arch` - ARCH/GARCH model implementations
- `statsmodels` - Statistical modeling
- `pyyaml` - YAML configuration file parsing
- `seaborn` - Statistical data visualization
- `scipy` - Scientific computing

## Configuration

The project uses YAML configuration files located in the `configs/` directory. The default configuration (`configs/default.yaml`) includes:

- **Data settings**: SPY ticker symbol, date ranges, and file paths
- **Model parameters**: GARCH model specifications (to be extended)

Example configuration:
```yaml
data:
  root_dir: "data"
  spy_prices_file: "data/spy/spy_prices.csv"
  spy_ticker: "SPY"
  start_date: "2010-01-01"
  end_date: null  # null = use today's date when running
```

## Usage

### Loading SPY Data

The package provides utilities to download and update SPY price data from Yahoo Finance:

```python
from spy_volatility.utils.config import load_config
from spy_volatility.data.loaders import load_or_update_spy_prices

# Load configuration
cfg = load_config()

# Load or update SPY prices
spy_data = load_or_update_spy_prices(cfg)
print(spy_data.tail())
```

The `load_or_update_spy_prices` function:
- Downloads full history if no data file exists
- Incrementally updates existing data with new records
- Automatically handles date ranges and deduplication

### Running Test Script

Test the data loading functionality:
```bash
python scripts/test_load_spy.py
```

## Features

- **Automated Data Download**: Download SPY historical prices from Yahoo Finance
- **Incremental Updates**: Automatically update existing datasets with new data
- **GARCH Models**: Framework for implementing GARCH volatility models
- **Configuration Management**: YAML-based configuration system
- **Modular Design**: Clean separation of data, models, and utilities

## Development

The project follows a modular structure:
- **Data Module** (`spy_volatility.data`): Handles data loading and preprocessing
- **Models Module** (`spy_volatility.models`): Contains GARCH and volatility model implementations
- **Training Module** (`spy_volatility.training`): Model training and evaluation utilities
- **Utils Module** (`spy_volatility.utils`): Configuration and helper functions

## License

[Add your license information here]

## Author

[Add author information here]




