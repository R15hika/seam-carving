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
    raise NotImplementedError("Person 2: implement find_seam_dp")
