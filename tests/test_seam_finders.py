"""
Tests for Persons 2, 3, 4: every seam finder must return a valid seam,
and DP / graph cut must match a brute-force optimum on tiny images.
"""
import itertools

import numpy as np
import pytest

from seamcarve.dp import find_seam_dp
from seamcarve.greedy import find_seam_greedy
from seamcarve.graphcut import find_seam_graphcut

ALL_FINDERS = [find_seam_dp, find_seam_greedy, find_seam_graphcut]
OPTIMAL_FINDERS = [find_seam_dp, find_seam_graphcut]


def is_valid_seam(seam, h, w):
    seam = np.asarray(seam)
    return (len(seam) == h
            and ((seam >= 0) & (seam < w)).all()
            and (np.abs(np.diff(seam)) <= 1).all())


def brute_force_min_cost(energy):
    """Try every possible seam (exponential - only for tiny images)."""
    h, w = energy.shape
    best = np.inf
    for start in range(w):
        for moves in itertools.product((-1, 0, 1), repeat=h - 1):
            cols = [start]
            for m in moves:
                cols.append(cols[-1] + m)
            if all(0 <= c < w for c in cols):
                best = min(best, sum(energy[i, c] for i, c in enumerate(cols)))
    return best


def seam_cost(energy, seam):
    return sum(energy[i, c] for i, c in enumerate(seam))


@pytest.mark.parametrize("finder", ALL_FINDERS)
def test_seam_is_valid(finder):
    energy = np.random.rand(15, 12)
    assert is_valid_seam(finder(energy), 15, 12)


@pytest.mark.parametrize("finder", ALL_FINDERS)
def test_single_column(finder):
    energy = np.random.rand(5, 1)
    assert list(finder(energy)) == [0] * 5


@pytest.mark.parametrize("finder", OPTIMAL_FINDERS)
@pytest.mark.parametrize("seed", range(5))
def test_matches_brute_force(finder, seed):
    rng = np.random.default_rng(seed)
    energy = rng.random((5, 4))
    seam = finder(energy)
    assert is_valid_seam(seam, 5, 4)
    assert np.isclose(seam_cost(energy, seam), brute_force_min_cost(energy))
