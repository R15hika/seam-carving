"""Tests for Person 1: energy map, seam removal, transpose, resize."""
import numpy as np

from seamcarve.energy import compute_energy
from seamcarve.carve import remove_seam, transpose


def test_energy_shape_and_nonnegative():
    img = np.random.randint(0, 256, (20, 30, 3), dtype=np.uint8)
    e = compute_energy(img)
    assert e.shape == (20, 30)
    assert (e >= 0).all()


def test_flat_image_has_zero_energy():
    img = np.full((10, 10, 3), 128, dtype=np.uint8)
    assert np.allclose(compute_energy(img), 0)


def test_edge_has_high_energy():
    # left half black, right half white -> energy peaks at the boundary
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[:, 5:] = 255
    e = compute_energy(img)
    assert e[:, 4:6].mean() > e[:, :3].mean()


def test_remove_seam_shape():
    img = np.random.randint(0, 256, (5, 8, 3), dtype=np.uint8)
    seam = np.array([0, 1, 2, 3, 4])
    assert remove_seam(img, seam).shape == (5, 7, 3)


def test_remove_seam_removes_correct_pixels():
    img = np.arange(12).reshape(3, 4)          # 2-D for easy checking
    seam = np.array([0, 1, 3])
    expected = np.array([[1, 2, 3],
                         [4, 6, 7],
                         [8, 9, 10]])
    assert np.array_equal(remove_seam(img, seam), expected)


def test_transpose_roundtrip():
    img = np.random.randint(0, 256, (4, 6, 3), dtype=np.uint8)
    t = transpose(img)
    assert t.shape == (6, 4, 3)
    assert np.array_equal(transpose(t), img)
