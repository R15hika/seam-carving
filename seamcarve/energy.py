"""
Energy map  --  OWNER: Rishika Bimal Attodi

The energy of a pixel says how "important" it is. High energy = edges/detail
(keep these), low energy = flat areas like sky (safe to remove).
"""
import numpy as np
import cv2


def compute_energy(img: np.ndarray) -> np.ndarray:
    """
    Compute the energy map of an image.

    Args:
        img: H x W x 3 uint8 image (BGR, as loaded by cv2.imread).

    Returns:
        H x W float64 array, energy[i, j] >= 0.

    TODO (Person 1):
        1. Convert to grayscale:        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        2. Convert to float64 so negative gradients don't overflow.
        3. Gradient in x and y:          cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                                         cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        4. Combine:  np.abs(dx) + np.abs(dy)   (L1)   or   np.sqrt(dx**2 + dy**2)  (L2)
           Pick one and justify it in the report.
    """
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    gray = gray.astype(np.float64)
    dx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    # L1 norm (Avidan & Shamir's e1): cheaper than L2, same edge ranking in practice.
    return np.abs(dx) + np.abs(dy)
