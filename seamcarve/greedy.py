"""
Greedy seam finder  --  OWNER: Person 3
"""
import numpy as np
from .energy import compute_energy

def find_seam_greedy(energy: np.ndarray) -> np.ndarray:
    """
    Find a vertical seam greedily: start at the min-energy pixel in row 0,
    then in each next row move to the lowest of the (up to) 3 neighbours below.

    Args:
        energy: H x W float array.

    Returns:
        length-H int array, seam[i] = column in row i.
    """

    height, width = energy.shape
    seam = np.empty(height, dtype=np.intp)

    seam[0] = np.argmin(energy[0])

    for row in range(1, height):
        previous_col = seam[row - 1]
        start_col = max(0, previous_col - 1)
        end_col = min(width, previous_col + 2)

        neighbours = energy[row, start_col:end_col]
        seam[row] = start_col + np.argmin(neighbours)

    return seam
