"""
Graph cut (min-cut / max-flow) seam finder  --  OWNER: Nurafifah Binte Jasmani

See item 4 of the assignment for the graph construction.
Note: this is slow (Edmonds-Karp is O(V E^2)) - test on small images (~50x50).
"""
from collections import deque

import numpy as np

# Finds the lowest energy seam (same goal as DP, different method).
# 1. Pixels become nodes, arrows link each pixel to the one on its right.
#    Arrow cost = that pixel's energy.
# 2. Cheapest set of arrows that cuts left side from right side = the seam.
# 3. Max flow (Edmonds-Karp) finds that cut, since max flow = min cut.

INF = float("inf")   # "can never be cut" - used for the rule arrows


# The graph: dots, arrows, and how much room each arrow has left.
class FlowNetwork:

    # Make an empty graph with n_nodes dots and no arrows yet.
    def __init__(self, n_nodes: int):
        self.n = n_nodes
        self.adj = [[] for _ in range(n_nodes)]  # adj[u] = arrows leaving dot u
        self.to = []                              # to[e] = dot that arrow e points to
        self.residual = []                        # residual[e] = room left on arrow e

    # Add an arrow u -> v, plus an "undo" arrow v -> u (starts with 0 room).
    # Arrow e and its undo arrow are stored next to each other: e and e ^ 1.
    def add_edge(self, u: int, v: int, capacity: float) -> None:
        self.adj[u].append(len(self.to))
        self.to.append(v)
        self.residual.append(capacity)
        # undo arrow, starts at 0
        self.adj[v].append(len(self.to))
        self.to.append(u)
        self.residual.append(0.0)

    # Starting from dot s, find every dot reachable using arrows that still
    # have room. Returns parent_edge[v] = arrow used to reach v (-1 = not reached).
    def bfs(self, s: int, eps: float):
        parent_edge = [-1] * self.n
        parent_edge[s] = -2
        q = deque([s])
        while q:
            u = q.popleft()
            for e in self.adj[u]:
                v = self.to[e]
                if parent_edge[v] == -1 and self.residual[e] > eps:
                    parent_edge[v] = e
                    q.append(v)
        return parent_edge

    # Edmonds-Karp: keep sending flow from s to t until no route has room left.
    def max_flow(self, s: int, t: int, eps: float = 0.0) -> float:
        flow = 0.0
        while True:
            # find the shortest route from s to t that still has room
            parent_edge = self.bfs(s, eps)
            if parent_edge[t] == -1:      # no route left -> done
                return flow

            # x = the smallest room on that route (the bottleneck)
            x = INF
            v = t
            while v != s:
                e = parent_edge[v]
                x = min(x, self.residual[e])
                v = self.to[e ^ 1]

            # send x along the route: less room forwards, more room on undo arrows
            v = t
            while v != s:
                e = parent_edge[v]
                self.residual[e] -= x
                self.residual[e ^ 1] += x
                v = self.to[e ^ 1]
            flow += x


# Steps 1-4: turn the energy map into dots and arrows.
def build_seam_graph(energy: np.ndarray) -> FlowNetwork:
    h, w = energy.shape
    # Step 1: one dot per pixel, plus START (s) and END (t)
    s, t = h * w, h * w + 1
    g = FlowNetwork(h * w + 2)

    # Dot number of pixel (row i, column j).
    def node(i, j):
        return i * w + j

    for i in range(h):
        # Step 2: START -> first pixel of every row (can't be cut)
        g.add_edge(s, node(i, 0), INF)

        for j in range(w):
            if j + 1 < w:
                # Step 3: arrow to the right pixel, cost = this pixel's energy
                g.add_edge(node(i, j), node(i, j + 1), float(energy[i, j]))
                # Step 3: rule arrow backwards (can't be cut)
                #         -> only ONE pixel per row gets cut
                g.add_edge(node(i, j + 1), node(i, j), INF)
            else:
                # Step 2: last pixel of every row -> END.
                # Cost = its energy (brief says inf, but then the last column
                # could never be removed).
                g.add_edge(node(i, j), t, float(energy[i, j]))

            # Step 4: rule arrows to the rows above and below (can't be cut)
            #         -> the seam stays connected between rows
            if j >= 1:
                if i >= 1:
                    g.add_edge(node(i, j), node(i - 1, j - 1), INF)
                if i + 1 < h:
                    g.add_edge(node(i, j), node(i + 1, j - 1), INF)
    return g


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
    energy = np.asarray(energy, dtype=np.float64)
    h, w = energy.shape
    s, t = h * w, h * w + 1
    # treat tiny leftovers from decimal rounding as 0
    eps = 1e-9 * (float(energy.sum()) + 1.0)

    # Steps 1-4: build the dots and arrows
    g = build_seam_graph(energy)

    # Step 5: send as much flow as possible -> the cheapest arrows get full
    g.max_flow(s, t, eps)

    # Step 6: see which pixels START can still reach. In each row, the
    # rightmost reachable pixel sits just before the full (cut) arrow,
    # so that's the pixel to remove.
    reached = g.bfs(s, eps)
    seam = np.empty(h, dtype=np.intp)
    for i in range(h):
        j = w - 1
        while reached[i * w + j] == -1:
            j -= 1
        seam[i] = j
    return seam
