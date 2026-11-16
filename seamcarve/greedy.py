"""
Greedy seam finder  --  OWNER: Person 3
"""
import numpy as np


def find_seam_greedy(energy: np.ndarray) -> np.ndarray:
    """
    Find a vertical seam greedily: start at the min-energy pixel in row 0,
    then in each next row move to the lowest of the (up to) 3 neighbours below.

    Args:
        energy: H x W float array.

    Returns:
        length-H int array, seam[i] = column in row i.
    """
    raise NotImplementedError("Person 3: implement find_seam_greedy")
