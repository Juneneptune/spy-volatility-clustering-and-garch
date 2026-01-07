from spy_volatility.data.features import compute_returns, compute_realized_volatility
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.loaders import load_or_update_spy_prices
import matplotlib.pyplot as plt

def main() -> None:
    # Load config and data
    cfg = load_config()
    prices = load_or_update_spy_prices(cfg, allow_data_update=False)

    # Compute returns
    prices = compute_returns(prices)
    rv = compute_realized_volatility(prices)

    root = get_project_root()

    rv.plot(figsize=(10, 5), title="Realized Volatility")
    plt.savefig(f"{root}/data/outputs/figures/SPY_realized_volatility.png")
    plt.close()
    prices["SPY_Log_Return"].plot(figsize=(10, 5), title="Log Returns")
    plt.savefig(f"{root}/data/outputs/figures/SPY_log_returns.png")
    plt.close()

if __name__ == "__main__":
    main()