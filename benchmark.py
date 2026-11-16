"""
Timing comparison and energy evaluation -- OWNER: Celest
Run with: python benchmark.py images/your_image.jpg
"""
import os
import sys
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np

from seamcarve.energy import compute_energy
from seamcarve.dp import find_seam_dp
from seamcarve.greedy import find_seam_greedy
from seamcarve.graphcut import find_seam_graphcut


def calculate_seam_energy(energy, seam):
    """Compute the total cost/energy of a given seam."""
    return sum(energy[i, c] for i, c in enumerate(seam))

def main(path):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read {path}, using synthetic energy matrices for benchmarking.")
        img = None

    finders = {
        "Greedy": find_seam_greedy,
        "Dynamic Programming": find_seam_dp,
        "Graph Cut": find_seam_graphcut
    }
    test_dims = [(50, 50), (100, 100), (150, 150), (200, 200)]
    results = {name: {"pixels": [], "times": [], "energies": []} for name in finders}
    os.makedirs("output", exist_ok=True)

    print(f"{'Algorithm':<22} | {'Size (HxW)':<12} | {'Time (s)':<10} | {'Total Energy':<12}")
    print("-" * 65)

    for h, w in test_dims:
        if img is not None:
            resized_img = cv2.resize(img, (w, h))
            energy = compute_energy(resized_img)
        else:
            energy = np.random.rand(h, w)
        num_pixels = h * w
        for name, finder in finders.items():
            t0 = time.perf_counter()
            try:
                seam = finder(energy)
                elapsed = time.perf_counter() - t0
                energy_val = calculate_seam_energy(energy, seam)
                
                results[name]["pixels"].append(num_pixels)
                results[name]["times"].append(elapsed)
                results[name]["energies"].append(energy_val)
                
                print(f"{name:<22} | {f'{h}x{w}':<12} | {elapsed:.6f}   | {energy_val:.2f}")
            except NotImplementedError:
                print(f"{name:<22} | {f'{h}x{w}':<12} | NOT IMPL   | N/A")
            except Exception as e:
                print(f"{name:<22} | {f'{h}x{w}':<12} | ERROR      | {e}")
    plt.figure(figsize=(10, 5))
    for name, data in results.items():
        if data["pixels"]:
            plt.plot(data["pixels"], data["times"], marker='o', label=name, linewidth=2)

    plt.title("Seam Carving Algorithm Runtime Comparison", fontsize=14, fontweight='bold')
    plt.xlabel("Number of Pixels ($H \\times W$)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    plot_path = os.path.join("output", "seam_carving_runtime_benchmark.png")
    plt.savefig(plot_path, dpi=300)
    print(f"\nRuntime benchmark plot successfully saved to '{plot_path}'")
    plt.close()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "images/sample.jpg")