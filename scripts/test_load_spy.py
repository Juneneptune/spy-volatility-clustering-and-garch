# scripts/test_load_spy.py

from spy_volatility.utils.config import load_config
from spy_volatility.data.loaders import load_or_update_spy_prices
import yfinance as yf



if __name__ == "__main__":
    cfg = load_config()
    spy = load_or_update_spy_prices(cfg, allow_data_update=False)

    print(spy.tail())