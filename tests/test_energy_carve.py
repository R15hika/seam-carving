# tests for person 1: energy map, seam removal, transpose and resize
import numpy as np
import pytest

from seamcarve.energy import compute_energy
from seamcarve.carve import remove_seam, transpose, resize

def leftmost_seam(energy):
    # dummy seam finder so resize can be tested without waiting on dp
    return np.zeros(energy.shape[0], dtype=int)

def test_energy_shape_and_nonnegative():
    img = np.random.randint(0, 256, (20, 30, 3), dtype=np.uint8)
    e = compute_energy(img)
    assert e.shape == (20, 30)
    assert (e >= 0).all()

def test_energy_works_on_grayscale():
    img = np.random.randint(0, 256, (20, 30), dtype=np.uint8)
    assert compute_energy(img).shape == (20, 30)

def test_flat_image_has_zero_energy():
    img = np.full((10, 10, 3), 128, dtype=np.uint8)
    assert np.allclose(compute_energy(img), 0)

def test_edge_has_high_energy():
    # left half black, right half white so energy should spike at the boundary
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[:, 5:] = 255
    e = compute_energy(img)
    assert e[:, 4:6].mean() > e[:, :3].mean()

def test_remove_seam_shape():
    img = np.random.randint(0, 256, (5, 8, 3), dtype=np.uint8)
    seam = np.array([0, 1, 2, 3, 4])
    assert remove_seam(img, seam).shape == (5, 7, 3)

def test_remove_seam_removes_correct_pixels():
    # 2d so it's easy to see which numbers went missing
    img = np.arange(12).reshape(3, 4)
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

def test_resize_width_and_height():
    img = np.random.randint(0, 256, (20, 30, 3), dtype=np.uint8)
    out = resize(img, 25, 15, leftmost_seam)
    assert out.shape == (15, 25, 3)
    assert out.dtype == np.uint8

def test_resize_same_size_does_nothing():
    img = np.random.randint(0, 256, (10, 12, 3), dtype=np.uint8)
    assert np.array_equal(resize(img, 12, 10, leftmost_seam), img)

def test_resize_calls_on_seam_for_every_seam():
    img = np.random.randint(0, 256, (10, 12, 3), dtype=np.uint8)
    calls = []
    resize(img, 9, 8, leftmost_seam, on_seam=lambda im, s, d: calls.append(d))
    assert calls == ["vertical"] * 3 + ["horizontal"] * 2

def test_resize_rejects_bad_sizes():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    with pytest.raises(ValueError):
        resize(img, 11, 10, leftmost_seam)
    with pytest.raises(ValueError):
        resize(img, 10, 0, leftmost_seam)
