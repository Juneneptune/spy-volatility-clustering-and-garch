import numpy as np
import pandas as pd

def try_cholesky(
    A: pd.DataFrame,
) -> bool:
    """
    Input: pd.DataFrame (square, symmetric)
    Output: bool
        - returns True if np.linalg.cholesky succeeds
        - returns False if it throws LinAlgError
        - does not modify input
    """
    A_np = A.to_numpy()

    if A_np.ndim != 2 or A_np.shape[0] != A_np.shape[1]:
        return False
    if not np.isfinite(A_np).all():
        return False

    try:
        np.linalg.cholesky(A_np)
        return True
    except np.linalg.LinAlgError:
        return False
    
def add_jitter(
    A: pd.DataFrame, 
    lam: float, 
    atol: float = 1e-5
) -> pd.DataFrame:
    """
    - Smallest-eigenvalue regularization via diagonal shift.
    - If matrix isn’t symmetric within tolerance, symmetrize: (A + A.T)/2
    """
    A_np = A.to_numpy()

    if not np.allclose(A_np, A_np.T, atol):
        A_np = (A_np + A_np.T) / 2
    
    A_np_reg = np.zeros_like(A_np)
    np.fill_diagonal(A_np_reg, lam) 
    
    A_np_reg += A_np

    A = pd.DataFrame(A_np_reg, A.index, A.columns)
    
    return A

def clip_eigenvalues(
    A: pd.DataFrame, 
    eps: float, 
    atol: float = 1e-5
) -> pd.DataFrame:
    """
    - Symmetrize first if larger than tolerance and clips min eigenvalue and reconstructs.
    """
    A_np = A.to_numpy()

    if not np.allclose(A_np, A_np.T, atol):
        A = (A_np + A_np.T) / 2

    eigval, eigvec = np.linalg.eigh(A)    

    eigval = np.maximum(eigval, eps)
    eigval_mat = np.zeros_like(eigvec)
    np.fill_diagonal(eigval_mat, eigval)
    A_np = eigvec @ eigval_mat @ eigvec.T
    A_np = (A_np + A_np.T) / 2 # One more symmetry repair

    A = pd.DataFrame(A_np, A.index, A.columns)
    return A