"""
Seam removal + resize driver  --  OWNER: Person 1

A seam is represented as a 1-D integer array of length H:
    seam[i] = column index of the pixel to remove in row i
(Every seam finder - DP, greedy, graph cut - must return this format.)
"""
import numpy as np

from .energy import compute_energy


def remove_seam(img: np.ndarray, seam: np.ndarray) -> np.ndarray:
    """
    Remove one vertical seam from the image.

    Args:
        img:  H x W x C (or H x W) array.
        seam: length-H int array, seam[i] in [0, W-1].

    Returns:
        H x (W-1) x C (or H x (W-1)) array.

    TODO (Person 1):
        Build a boolean mask of shape H x W that is True everywhere
        except at (i, seam[i]), then use it to select the remaining pixels
        and reshape to (H, W-1, C).
        Hint: mask = np.ones((H, W), dtype=bool); mask[np.arange(H), seam] = False
    """
    raise NotImplementedError("Person 1: implement remove_seam")


def transpose(img: np.ndarray) -> np.ndarray:
    """
    Swap rows and columns so horizontal seams can be found with the
    vertical-seam code. Works for both H x W and H x W x C arrays.

    TODO (Person 1):  np.transpose(img, (1, 0, 2)) for colour, img.T for 2-D.
    """
    raise NotImplementedError("Person 1: implement transpose")


def resize(img: np.ndarray, new_w: int, new_h: int, find_seam, on_seam=None) -> np.ndarray:
    """
    Shrink img to new_w x new_h by repeatedly removing seams.

    Args:
        img:       H x W x 3 uint8 image.
        new_w:     target width  (<= current width).
        new_h:     target height (<= current height).
        find_seam: function(energy) -> seam   (dp / greedy / graphcut).
        on_seam:   optional callback(img, seam, direction) called before each
                   removal - used by the app for step-by-step visualisation.

    TODO (Person 1):
        while width > new_w:
            energy = compute_energy(img); seam = find_seam(energy)
            img = remove_seam(img, seam)
        then for height: transpose, do the same loop, transpose back.
    """
    raise NotImplementedError("Person 1: implement resize")
