from spy_volatility.models.garch_models import fit_garch_11
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.loaders import load_or_update_spy_prices
from spy_volatility.data.features import compute_realized_volatility, compute_returns
import matplotlib.pyplot as plt
import pandas as pd

def main() -> None:
    
    # Load configs & SPY data
    cfg = load_config()
    root = get_project_root()
    prices = load_or_update_spy_prices(cfg, allow_data_update=False)

    # Compute realized volatility and GARCH(1, 1) predicted volatility
    prices_with_returns = compute_returns(prices, price_col="SPY_Adj_Close")
    returns = prices_with_returns["SPY_Log_Return"]
    rv21 = compute_realized_volatility(prices_with_returns, window=21).dropna()
    garch11_cond_vol = fit_garch_11(returns.dropna())

    # Concat rv21 and GARCH
    rv_vs_garch = pd.concat([rv21, garch11_cond_vol], axis=1)
    rv_vs_garch.columns = ["RV21", "GARCH11"]
    rv_vs_garch = rv_vs_garch.dropna()

    
    ax = rv_vs_garch.plot(figsize=(10, 5))
    ax.set_title("Volatility Comparison")
    ax.set_ylabel("Annualized Volatility")
    ax.legend()

    plt.savefig(f"{root}/data/outputs/figures/SPY_GARCH11_VS_RV21.png")
    plt.close()

if __name__ == "__main__":
    main()