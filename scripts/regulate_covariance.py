from spy_volatility.data.loaders import load_or_update_prices
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.features import compute_returns
from spy_volatility.risk.cov_metrics import rolling_sample_covariance, covariance_diagnostics
from spy_volatility.risk.spd import try_cholesky, add_jitter, clip_eigenvalues
import pandas as pd
import matplotlib.pyplot as plt

# Load data
cfg = load_config("default_multivar.yaml")
prices = load_or_update_prices(cfg, allow_data_update=False, show_only_adj_close=True)

root = get_project_root()

# Compute covariance of returns
returns = compute_returns(prices, price_col=prices.columns).dropna()
rolling_cov = rolling_sample_covariance(returns, window=63)

# Diagnostic with covariance regularization
log = []
for date in rolling_cov:
    cov_raw = rolling_cov[date]
    cov_jit = add_jitter(cov_raw, lam=1e-6)
    cov_clip = clip_eigenvalues(cov_raw, eps=1e-6) 
    raw_diag  = covariance_diagnostics(cov_raw)
    jit_diag  = covariance_diagnostics(cov_jit)
    clip_diag = covariance_diagnostics(cov_clip)

    log.append({
        "date": date,

        "raw_min_eig":  raw_diag["min_eigenvalue"],
        "raw_cond":     raw_diag["condition_number"],
        "raw_chol_ok":  try_cholesky(cov_raw),

        "jit_min_eig":  jit_diag["min_eigenvalue"],
        "jit_cond":     jit_diag["condition_number"],
        "jit_chol_ok":  try_cholesky(cov_jit),

        "clip_min_eig": clip_diag["min_eigenvalue"],
        "clip_cond":    clip_diag["condition_number"],
        "clip_chol_ok": try_cholesky(cov_clip),
        })
log = pd.DataFrame(log)

fig, ax = plt.subplots(1, 1, figsize=(12, 5))

ax.plot(log.index, log["raw_cond"], label="Raw", alpha=0.8)
ax.plot(log.index, log["jit_cond"], label="Jittered", alpha=0.8)
ax.plot(log.index, log["clip_cond"], label="Clipped", alpha=0.8)

ax.set_title("Condition Number of Rolling Covariance (Regularized)")
ax.set_ylabel("Condition Number")
ax.set_xlabel("Date")

ax.legend()
ax.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(
    f"{root}/data/outputs/figures/regularized_covariance_condition_number.png",
    dpi=150
)
plt.close()

print(
    f"Saved figure: {root}/data/outputs/figures/"
    "regularized_covariance_condition_number.png"
)
