from spy_volatility.data.loaders import load_or_update_prices
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.features import compute_returns
from spy_volatility.risk.cov_metrics import rolling_sample_covariance, covariance_diagnostics
import pandas as pd
import matplotlib.pyplot as plt

def main() -> None:
    # load cfg for multivariate price data
    root = get_project_root()
    cfg = load_config("default_multivar.yaml")
    prices = load_or_update_prices(cfg, allow_data_update=False, show_only_adj_close=True)

    # compute returns and drop missing values
    returns = compute_returns(
        prices = prices, 
        price_col = list(prices.columns)
        ).dropna()

    # Compute rolling covariance and collect diagnoistic of sample covariance
    cov = rolling_sample_covariance(returns, window=63)  # Roughly 3 months
    rolling_diagnostic = pd.DataFrame(columns=[
        "min_eigenvalue", 
        "max_eigenvalue", 
        "condition_number"
        ])

    for date in cov.keys():
        rolling_diagnostic.loc[date] = covariance_diagnostics(cov[date])

    ### More Efficient ###
    # rows = []

    # for date, cov_t in cov.items():
    #     diag = covariance_diagnostics(cov_t)
    #     rows.append({
    #         "date": date,
    #         "min_eigenvalue": diag["min_eigenvalue"],
    #         "max_eigenvalue": diag["max_eigenvalue"],
    #         "condition_number": diag["condition_number"],
    #     })

    # rolling_diagnostic = (
    #     pd.DataFrame(rows)
    #     .set_index("date")
    # )

    # Plot covariance diagnostic vs time
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10, 8))

    rolling_diagnostic["min_eigenvalue"].plot(ax=axes[0], title="Min Eigenvalue")
    rolling_diagnostic["max_eigenvalue"].plot(ax=axes[1], title="Max Eigenvalue")
    rolling_diagnostic["condition_number"].plot(ax=axes[2], title="Condition Number")

    plt.tight_layout()
    plt.savefig(f"{root}/data/outputs/figures/prices_covariance_fragility.png")
    plt.close()


if __name__ == "__main__":
    main()
