import pandas as pd
import numpy as np

def compute_returns(
    prices: pd.DataFrame,
    price_col: str = "SPY_Adj_Close",
) -> pd.DataFrame:
    # Find stock name
    ticker = price_col.split("_")[0]

    # Compute log return and squared return
    log_adj_close = np.log(prices[price_col])
    prices[ticker + "_Log_Return"] = log_adj_close.diff()
    prices[ticker + "_Squared_Return"] = log_adj_close.diff() ** 2
    return prices

def compute_realized_volatility(
    returns: pd.DataFrame,
    window: int = 21,
    annualization: int = 252,
) -> pd.Series:

    # Find stock name
    ticker = returns.columns[-1].split("_")[0]

    if ticker + "_Log_Return" not in returns.columns:
        raise KeyError(
            f"Required column '{ticker + "_Log_Return"}' not found. "
            f"Available columns: {list(returns.columns)}"
        )

    if ticker + "_Squared_Return" not in returns.columns:
        raise KeyError(
            f"Required column '{ticker + "_Squared_Return"}' not found. "
            f"Available columns: {list(returns.columns)}"
        )

    vol = np.sqrt(annualization * returns[ticker + "_Squared_Return"].rolling(window).mean())

    return vol
