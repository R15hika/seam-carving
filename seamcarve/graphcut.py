"""
Graph cut (min-cut / max-flow) seam finder  --  OWNER: Person 4

See item 4 of the assignment for the graph construction.
Note: this is slow (Edmonds-Karp is O(V E^2)) - test on small images (~50x50).
"""
import numpy as np


def find_seam_graphcut(energy: np.ndarray) -> np.ndarray:
    """
    Find the minimum-energy vertical seam via min s-t cut.

    Args:
        energy: H x W float array.

    Returns:
        length-H int array, seam[i] = column in row i.

    Steps:
        1. Build graph: node per pixel + source + sink.
        2. source -> column 0 (inf), column W-1 -> sink (inf).
        3. (i,j) -> (i,j+1) with capacity e[i,j];  (i,j+1) -> (i,j) inf.
        4. Diagonal inf edges (i,j) -> (i-1,j-1) and (i,j) -> (i+1,j-1).
        5. Run Edmonds-Karp max flow.
        6. BFS from source in residual graph; in each row the rightmost
           reachable pixel is the seam pixel.
    """
    raise NotImplementedError("Person 4: implement find_seam_graphcut")
