import pandas as pd
import numpy as np
from spy_volatility.data.loaders import _filter_columns_by_suffix

def rolling_sample_covariance(
    returns: pd.DataFrame,
    window: int,
) -> dict[pd.Timestamp, pd.DataFrame]:
    """
    Computes rolling sample covariance
    """
    date_cov_dict = {}

    # Filter just log returns
    returns = _filter_columns_by_suffix(returns, suffix="_Log_Return")

    # Remove Log_Return name from columns
    assets = returns.columns.str.replace("_Log_Return", "", regex=False)

    # Split into windows and compute covariance
    for idx in range(window, len(returns)):
        window_returns = returns.iloc[idx - window: idx]
        x = window_returns.to_numpy()
        x_centered = x - x.mean(axis=0)  # Center data
        cov = x_centered.T @ x_centered / (window - 1)  # Windowing reduced by 1 due to getting the mean from the data may need to remove later for MLE training
        date_cov_dict[returns.index[idx]] = pd.DataFrame(cov, index=assets, columns=assets)  # Add into date dict
    return date_cov_dict  
        
def covariance_diagnostics(
    cov: pd.DataFrame,
) -> dict[str, float]:
    """
    returns:
        - smallest eigenvalue
        - largest eigenvalue
        - condition number
    """
    x = cov.to_numpy()
    eig = np.linalg.eigvals(x)
    return {
        "min_eigenvalue": eig.min(),
        "max_eigenvalue": eig.max(),
        "condition_number": eig.max() / eig.min(),
    }