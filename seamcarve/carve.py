"""
Seam removal + resize driver  --  OWNER: Person 1

A seam is represented as a 1-D integer array of length H:
    seam[i] = column index of the pixel to remove in row i
(Every seam finder - DP, greedy, graph cut - must return this format.)
"""
import numpy as np

import cv2

from .energy import compute_energy


def load_image(path) -> np.ndarray:
    """
    Load an image from disk as an H x W x 3 uint8 BGR array.

    Uses np.fromfile + cv2.imdecode instead of cv2.imread so paths with
    spaces / non-ASCII characters work on Windows.
    """
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Could not read image: {path}")
    return img


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
    h, w = img.shape[:2]
    seam = np.asarray(seam, dtype=np.intp)
    if seam.shape != (h,):
        raise ValueError(f"seam must have length {h}, got shape {seam.shape}")
    if seam.min() < 0 or seam.max() >= w:
        raise ValueError(f"seam indices must be in [0, {w - 1}]")
    mask = np.ones((h, w), dtype=bool)
    mask[np.arange(h), seam] = False
    return img[mask].reshape((h, w - 1) + img.shape[2:])


def transpose(img: np.ndarray) -> np.ndarray:
    """
    Swap rows and columns so horizontal seams can be found with the
    vertical-seam code. Works for both H x W and H x W x C arrays.

    TODO (Person 1):  np.transpose(img, (1, 0, 2)) for colour, img.T for 2-D.
    """
    if img.ndim == 3:
        return np.ascontiguousarray(np.transpose(img, (1, 0, 2)))
    return np.ascontiguousarray(img.T)


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
    h, w = img.shape[:2]
    if not (1 <= new_w <= w and 1 <= new_h <= h):
        raise ValueError(f"target {new_w}x{new_h} must be between 1x1 and {w}x{h}")

    # Vertical seams -> reduce width.
    while img.shape[1] > new_w:
        seam = find_seam(compute_energy(img))
        if on_seam is not None:
            on_seam(img, seam, "vertical")
        img = remove_seam(img, seam)

    # Horizontal seams -> transpose, remove vertical seams, transpose back.
    if img.shape[0] > new_h:
        img = transpose(img)
        while img.shape[1] > new_h:
            seam = find_seam(compute_energy(img))
            if on_seam is not None:
                # seam is in transposed coords: seam[j] = row removed in column j
                on_seam(transpose(img), seam, "horizontal")
            img = remove_seam(img, seam)
        img = transpose(img)

    return img
