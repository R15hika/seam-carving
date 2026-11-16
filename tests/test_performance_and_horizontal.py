import numpy as np
import pytest
from seamcarve.dp import find_seam_dp
from seamcarve.greedy import find_seam_greedy
from seamcarve.graphcut import find_seam_graphcut
from seamcarve.carve import transpose, resize

@pytest.mark.parametrize("finder", [find_seam_dp, find_seam_greedy, find_seam_graphcut])
def test_horizontal_seam_via_transpose(finder):
    energy = np.random.rand(10, 20)
    seam = finder(energy)
    assert len(seam) == 10
    assert (seam >= 0).all() and (seam < 20).all()

@pytest.mark.parametrize("finder", [find_seam_dp, find_seam_greedy, find_seam_graphcut])
def test_constant_energy_image(finder):
    energy = np.ones((10, 10)) * 5.0
    seam = finder(energy)
    assert len(seam) == 10
    assert (np.abs(np.diff(seam)) <= 1).all()

def test_full_pipeline_dp_integration():
    from seamcarve.energy import compute_energy
    img = np.random.randint(0, 256, (30, 40, 3), dtype=np.uint8)
    resized = resize(img, 35, 25, find_seam_dp)
    assert resized.shape == (25, 35, 3)