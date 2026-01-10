import numpy as np
import pandas as pd
from spy_volatility.risk.spd import try_cholesky, add_jitter, clip_eigenvalues


def print_result(name, result):
    print(f"{name:<45}: {result}")


print("\n================ BASIC SPD CASES ================\n")

# --- Example 1: Simple diagonal SPD ---
spd_diag = pd.DataFrame([[3.0, 0.0],
                         [0.0, 1.0]])

print("SPD Diagonal Matrix:\n", spd_diag)
print_result("Cholesky succeeds", try_cholesky(spd_diag))


# --- Example 2: Simple correlated SPD ---
spd_simple = pd.DataFrame([[2.0, 1.0],
                           [1.0, 2.0]])

print("\nSPD Correlated Matrix:\n", spd_simple)
print_result("Cholesky succeeds", try_cholesky(spd_simple))


# --- Example 3: Random SPD ---
rng = np.random.default_rng(0)
A = rng.standard_normal((3, 3))
spd_random = pd.DataFrame(A @ A.T + 0.1 * np.eye(3))

print("\nRandom SPD Matrix:\n", spd_random)
print_result("Cholesky succeeds", try_cholesky(spd_random))


print("\n================ FAILURE MODES ================\n")

# --- Example 4: Singular (perfect dependence) ---
singular = pd.DataFrame([[1.0, 1.0],
                          [1.0, 1.0]])

print("Singular Matrix:\n", singular)
print_result("Cholesky succeeds", try_cholesky(singular))


# --- Example 5: Indefinite symmetric ---
indefinite = pd.DataFrame([[1.0, 2.0],
                            [2.0, -1.0]])

print("\nIndefinite Symmetric Matrix:\n", indefinite)
print_result("Cholesky succeeds", try_cholesky(indefinite))


# --- Example 6: Asymmetric ---
asymmetric = pd.DataFrame([[1.0, 2.0],
                            [1.9, 1.0]])

print("\nAsymmetric Matrix:\n", asymmetric)
print_result("Cholesky succeeds", try_cholesky(asymmetric))


print("\n================ JITTER BEHAVIOR ================\n")

lam = 1e-6

print("Applying jitter to singular matrix (lam = 1e-6)")
singular_jit = add_jitter(singular, lam)

print("Jittered Matrix:\n", singular_jit)
print_result("Cholesky succeeds after jitter", try_cholesky(singular_jit))


print("\n================ CLIP BEHAVIOR ================\n")

# eigenvalues: 5, -1
needs_clip = pd.DataFrame([[2.0, 3.0],
                            [3.0, 2.0]])

print("Matrix with negative eigenvalue:\n", needs_clip)
print_result("Cholesky succeeds before clip", try_cholesky(needs_clip))

clipped = clip_eigenvalues(needs_clip, eps=1e-6)

print("\nClipped Matrix:\n", clipped)
print_result("Cholesky succeeds after clip", try_cholesky(clipped))


print("\n================ NEAR SINGULAR NUMERICS ================\n")

near_singular = pd.DataFrame([[1.0, 0.999999],
                               [0.999999, 0.999998]])

print("Near singular matrix:\n", near_singular)
print_result("Cholesky succeeds", try_cholesky(near_singular))

if not try_cholesky(near_singular):
    near_jit = add_jitter(near_singular, 1e-8)
    print("\nAfter small jitter:\n", near_jit)
    print_result("Cholesky succeeds after jitter", try_cholesky(near_jit))


print("\n================ DONE ================\n")
