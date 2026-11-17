"""
Dynamic programming seam finder  --  OWNER: Person 2
"""
import numpy as np


def find_seam_dp(energy: np.ndarray) -> np.ndarray:
    """
    Find the minimum-energy vertical seam using dynamic programming.

    Args:
        energy: H x W float array.

    Returns:
        length-H int array, seam[i] = column in row i.

    Recurrence:
        M[0][j] = e[0][j]
        M[i][j] = e[i][j] + min(M[i-1][j-1], M[i-1][j], M[i-1][j+1])
    Then backtrack from argmin of the last row.
    """
    energy = np.asarray(energy, dtype=np.float64)
    if energy.ndim != 2:
        raise ValueError(f"energy must be a 2-D array, got shape {energy.shape}")
    h, w = energy.shape
    if h == 0 or w == 0:
        raise ValueError("energy must be non-empty")

    # dp[i, j] stores the minimum cumulative cost of any seam that ends at (i, j).
    dp = np.empty((h, w), dtype=np.float64)
    # parent[i, j] stores which column in row i-1 led to the optimal dp[i, j].
    parent = np.empty((h, w), dtype=np.intp)

    dp[0] = energy[0]
    parent[0] = -1

    for i in range(1, h):
        for j in range(w):
            left = max(0, j - 1)
            right = min(w, j + 2)
            prev = dp[i - 1, left:right]

            best_prev_offset = int(np.argmin(prev))
            best_prev_col = left + best_prev_offset

            dp[i, j] = energy[i, j] + prev[best_prev_offset]
            parent[i, j] = best_prev_col

    seam = np.empty(h, dtype=np.intp)
    seam[-1] = int(np.argmin(dp[-1]))
    for i in range(h - 1, 0, -1):
        seam[i - 1] = parent[i, seam[i]]
    return seam


def find_seam_dp_horizontal(energy: np.ndarray) -> np.ndarray:
    """
    Find the minimum-energy horizontal seam.

    Args:
        energy: H x W float array.

    Returns:
        length-W int array, seam[j] = row in column j.
    """
    # Horizontal seam in (H, W) is equivalent to vertical seam in (W, H).
    return find_seam_dp(np.asarray(energy).T)
