# SPY Volatility Clustering and GARCH

A Python project for analyzing volatility clustering in SPY (S&P 500 ETF) data and implementing GARCH models for volatility forecasting.

## Project Structure

```
spy-volatility-clustering-and-garch/
├── configs/                    # Configuration files
│   └── default.yaml           # Default configuration for data loading and model parameters
│
├── data/                       # Data storage directory (created at runtime)
│   ├── spy/                   # SPY price data storage
│   │   └── spy_prices.csv     # Downloaded SPY historical prices (auto-generated)
│   └── outputs/               # Generated outputs
│       └── figures/           # Visualization outputs
│           ├── SPY_log_returns.png
│           ├── SPY_realized_volatility.png
│           └── SPY_GARCH11_VS_RV21.png
│
├── datasets/                   # Additional datasets (if any)
│
├── notebooks/                  # Jupyter notebooks for analysis
│   └── volatility_basics.ipynb
│
├── scripts/                    # Utility scripts
│   ├── test_load_spy.py       # Script to test SPY data loading
│   ├── print_config.py        # Print configuration settings
│   ├── compute_returns_and_rv.py  # Compute returns and realized volatility
│   └── fit_garch.py           # Fit GARCH(1,1) model and compare with RV
│
├── src/                        # Source code
│   └── spy_volatility/        # Main package
│       ├── __init__.py
│       ├── data/              # Data loading and processing modules
│       │   ├── __init__.py
│       │   ├── loaders.py    # SPY data download and loading utilities
│       │   └── features.py   # Feature engineering (returns, realized volatility)
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
- `matplotlib` - Plotting and visualization
- `yfinance` - Yahoo Finance data download
- `arch` - ARCH/GARCH model implementations
- `statsmodels` - Statistical modeling
- `pyyaml` - YAML configuration file parsing

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

### Computing Returns and Realized Volatility

Compute log returns and realized volatility from SPY prices:

```python
from spy_volatility.data.features import compute_returns, compute_realized_volatility
from spy_volatility.utils.config import load_config
from spy_volatility.data.loaders import load_or_update_spy_prices

# Load data
cfg = load_config()
prices = load_or_update_spy_prices(cfg, allow_data_update=False)

# Compute returns
prices = compute_returns(prices, price_col="SPY_Adj_Close")

# Compute realized volatility (21-day rolling window)
rv21 = compute_realized_volatility(prices, window=21)
```

Or run the script:
```bash
python scripts/compute_returns_and_rv.py
```

This script generates:
- `SPY_log_returns.png` - Time series plot of log returns
- `SPY_realized_volatility.png` - Time series plot of realized volatility

### Fitting GARCH Models

Fit a GARCH(1,1) model to returns and compare with realized volatility:

```python
from spy_volatility.models.garch_models import fit_garch_11
from spy_volatility.data.features import compute_returns, compute_realized_volatility

# Compute returns
returns = compute_returns(prices)["SPY_Log_Return"]

# Fit GARCH(1,1) model
garch_vol = fit_garch_11(returns.dropna())

# Compute realized volatility for comparison
rv21 = compute_realized_volatility(prices, window=21)
```

Or run the script:
```bash
python scripts/fit_garch.py
```

This script generates:
- `SPY_GARCH11_VS_RV21.png` - Comparison plot of GARCH(1,1) conditional volatility vs. 21-day realized volatility

### Utility Scripts

**Print configuration:**
```bash
python scripts/print_config.py
```

**Test data loading:**
```bash
python scripts/test_load_spy.py
```

## Features

- **Automated Data Download**: Download SPY historical prices from Yahoo Finance
- **Incremental Updates**: Automatically update existing datasets with new data
- **Returns Computation**: Calculate log returns and squared returns from price data
- **Realized Volatility**: Compute rolling-window realized volatility (annualized)
- **GARCH Models**: Fit GARCH(1,1) models with t-distributed errors using the `arch` library
- **Volatility Comparison**: Compare GARCH conditional volatility with realized volatility
- **Visualization**: Generate time series plots for returns, realized volatility, and model comparisons
- **Configuration Management**: YAML-based configuration system
- **Modular Design**: Clean separation of data, models, and utilities

## Development

The project follows a modular structure:
- **Data Module** (`spy_volatility.data`): 
  - `loaders.py`: Handles SPY data download and loading from Yahoo Finance
  - `features.py`: Feature engineering functions for computing returns and realized volatility
- **Models Module** (`spy_volatility.models`): 
  - `garch_models.py`: GARCH model implementations (currently GARCH(1,1) with t-distributed errors)
- **Training Module** (`spy_volatility.training`): Model training and evaluation utilities (to be extended)
- **Utils Module** (`spy_volatility.utils`): 
  - `config.py`: Configuration loading and project root utilities

### Key Functions

**Data Features** (`spy_volatility.data.features`):
- `compute_returns()`: Computes log returns and squared returns from price data
- `compute_realized_volatility()`: Computes rolling-window realized volatility (annualized)

**GARCH Models** (`spy_volatility.models.garch_models`):
- `fit_garch_11()`: Fits a GARCH(1,1) model to returns and returns conditional volatility series

## License

[Add your license information here]

## Author

[Add author information here]




