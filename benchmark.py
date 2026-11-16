"""
Timing comparison  --  OWNER: Person 5
Run with:  python benchmark.py images/your_image.jpg

TODO (Person 5):
    - time find_seam_dp / greedy / graphcut on several image sizes
    - plot time vs number of pixels (matplotlib), save to output/
    - compare total seam energy of greedy vs DP
"""
import sys
import time

import cv2

from seamcarve.energy import compute_energy
from seamcarve.dp import find_seam_dp
from seamcarve.greedy import find_seam_greedy


def main(path):
    img = cv2.imread(path)
    if img is None:
        sys.exit(f"Could not read {path}")
    energy = compute_energy(img)
    for name, finder in [("DP", find_seam_dp), ("Greedy", find_seam_greedy)]:
        t0 = time.perf_counter()
        finder(energy)
        print(f"{name:8s} {time.perf_counter() - t0:.4f}s for one seam on {img.shape[1]}x{img.shape[0]}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "images/sample.jpg")
