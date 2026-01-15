from spy_volatility.data.loaders import load_or_update_prices, _filter_columns_by_suffix
from spy_volatility.utils.config import load_config, get_project_root
from spy_volatility.data.features import compute_returns
from spy_volatility.risk.cov_metrics import rolling_sample_covariance, covariance_diagnostics
from spy_volatility.risk.spd import try_cholesky, add_jitter, clip_eigenvalues
from statsmodels.tsa.api import VAR

def fit_var_1(
    returns: pd.DataFrame,
) -> dict[str, Any]:
    """
    Input:
        - returns
    Return a dictionary:
        - "model" → fitted VARResults
        - "residuals" → residual DataFrame
        - "innovation_cov" → residual covariance (DataFrame)
    """
    filtered_returns = _filter_columns_by_suffix(returns, "_Log_Return")
    filtered_returns.columns = filtered_returns.columns.str.replace("_Log_Return", "")

    model =  VAR(filtered_returns)
    results = model.fit(1) # 1-lag
    res = results.resid
    cov = results.resid.cov()

    return {
        "Model": results,
        "residuals": res,
        "innovation_cov": cov,
    }
