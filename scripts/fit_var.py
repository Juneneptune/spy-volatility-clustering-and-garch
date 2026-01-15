from spy_volatility.data.loaders import load_or_update_prices
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.features import compute_returns
from spy_volatility.models.var import fit_var_1
from spy_volatility.risk.cov_metrics import rolling_sample_covariance, covariance_diagnostics
from spy_volatility.risk.spd import try_cholesky, add_jitter, clip_eigenvalues
import pandas as pd
import matplotlib.pyplot as plt

def main() -> None:
    # Root directory
    root = get_project_root()

    # Load configs and multivariate stock data
    cfg = load_config("default_multivar.yaml")
    prices = load_or_update_prices(cfg, allow_data_update=False, show_only_adj_close=True)

    # Compute returns and compute VAR (innovation covariance)
    returns = compute_returns(prices, prices.columns).dropna()
    var = fit_var_1(returns)
    cov = var["innovation_cov"].dropna()

    # Compute diagnostic of min/max eignenvalues and conditional number
    innov_diagnostic = covariance_diagnostics(cov)
    print(
        f"VAR Innovative Covariance Diagnostics: \n"
        f"Min Eigenvalue: {innov_diagnostic["min_eigenvalue"]} \n"
        f"Max Eigenvalue: {innov_diagnostic["max_eigenvalue"]} \n"
        f"Condition Number: {innov_diagnostic["condition_number"]}"
        )
    print(f"Can apply Chelosky?: {try_cholesky(cov)}")

    # Rolling sample covariance diagnostics for comparison
    rolling_cov = rolling_sample_covariance(returns, window=63)

    rolling_diagnostic = pd.DataFrame(
        {
            date: covariance_diagnostics(cov_t)
            for date, cov_t in rolling_cov.items()
        }
    ).T

    # Plot rolling vs VAR diagnostics
    fig, axes = plt.subplots(
        3, 1,
        sharex=True,
        figsize=(16, 8)  # wide enough so text never overlaps
    )

    metrics = [
        ("min_eigenvalue", "Min Eigenvalue", "{:.2e}"),
        ("max_eigenvalue", "Max Eigenvalue", "{:.2e}"),
        ("condition_number", "Condition Number", "{:.1f}"),
    ]

    for ax, (key, title, fmt) in zip(axes, metrics):
        # Rolling curve
        rolling_diagnostic[key].plot(ax=ax, label="Rolling Sample")

        # VAR innovation horizontal line
        ax.axhline(
            innov_diagnostic[key],
            linestyle="--",
            color="black",
            linewidth=1.5,
            label="VAR Innovation",
        )

        # Numeric label pushed OUTSIDE to the right
        ax.text(
            1.01,  # outside the axes
            innov_diagnostic[key],
            fmt.format(innov_diagnostic[key]),
            transform=ax.get_yaxis_transform(),  # x in axes, y in data
            ha="left",
            va="center",
            fontsize=9,
            clip_on=False,
        )

        ax.set_title(title)
        ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(f"{root}/data/outputs/figures/rolling_vs_var_cov_diagnostics.png", bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    main()
