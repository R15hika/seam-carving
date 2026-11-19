"""
Timing comparison and energy evaluation -- OWNER: Chang Qi Xuan Celest
Run with: python benchmark.py images/your_image.png
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

MAX_GRAPHCUT_PIXELS = 10000


def calculate_seam_energy(energy, seam):
    return float(sum(energy[i, int(c)] for i, c in enumerate(seam)))

def main(path):
    img = cv2.imread(path)
    if img is None:
        print(f"Could not read {path}, using synthetic energy matrices for benchmarking.")
    finders = [
        ("Greedy", find_seam_greedy),
        ("Dynamic Programming", find_seam_dp),
        ("Graph Cut", find_seam_graphcut),
    ]
    test_dims = [(50, 50), (100, 100), (150, 150), (200, 200)]
    results = {
        name: {"labels": [], "pixels": [], "times": [], "energies": []}
        for name, _ in finders
    }
    os.makedirs("output", exist_ok=True)
    print(f"{'Algorithm':<22} | {'Size (HxW)':<12} | {'Time (s)':<10} | {'Total Energy':<12}")
    print("-" * 65)
    for h, w in test_dims:
        if img is not None:
            resized_img = cv2.resize(img, (w, h))
            energy = compute_energy(resized_img)
        else:
            rng = np.random.default_rng(h * 1000 + w)
            energy = rng.random((h, w))
        num_pixels = h * w
        size_label = f"{h}x{w}"
        for name, finder in finders:
            if name == "Graph Cut" and num_pixels > MAX_GRAPHCUT_PIXELS:
                print(f"{name:<22} | {size_label:<12} | {'SKIPPED':<10} | {'(>10k px)':<12}")
                continue
            t0 = time.perf_counter()
            try:
                seam = finder(energy)
                elapsed = time.perf_counter() - t0
                energy_val = calculate_seam_energy(energy, seam)
                results[name]["labels"].append(size_label)
                results[name]["pixels"].append(num_pixels)
                results[name]["times"].append(elapsed)
                results[name]["energies"].append(energy_val)
                print(f"{name:<22} | {size_label:<12} | {elapsed:<10.6f} | {energy_val:<12.2f}")
            except NotImplementedError:
                print(f"{name:<22} | {size_label:<12} | {'NOT IMPL':<10} | {'N/A':<12}")
            except Exception as e:
                print(f"{name:<22} | {size_label:<12} | {'ERROR':<10} | {e}")
    plt.figure(figsize=(10, 5))
    for name, data in results.items():
        if data["pixels"]:
            plt.plot(data["pixels"], data["times"], marker="o", label=name, linewidth=2)
    plt.title("Seam Carving Algorithm Runtime Comparison", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Pixels (H x W)", fontsize=12)
    plt.ylabel("Execution Time (seconds)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=11)
    plt.tight_layout()
    runtime_plot_path = os.path.join("output", "seam_carving_runtime_benchmark.png")
    plt.yscale("log")
    plt.savefig(runtime_plot_path, dpi=300, bbox_inches="tight")
    plt.close()
    active_algos = [name for name, data in results.items() if data["energies"]]
    if active_algos:
        common_labels = results[active_algos[0]]["labels"]
        for name in active_algos[1:]:
            if len(results[name]["labels"]) < len(common_labels):
                common_labels = results[name]["labels"]

        if common_labels:
            x = np.arange(len(common_labels))
            width = 0.8 / len(active_algos)

            plt.figure(figsize=(10, 5))
            for idx, name in enumerate(active_algos):
                energies_subset = results[name]["energies"][: len(common_labels)]
                offset = (idx - (len(active_algos) - 1) / 2) * width
                plt.bar(x + offset, energies_subset, width=width, label=name)

            plt.title("Total Seam Energy by Image Size", fontsize=14, fontweight="bold")
            plt.xlabel("Image Size (H x W)", fontsize=12)
            plt.ylabel("Total Seam Energy", fontsize=12)
            plt.xticks(x, common_labels)
            plt.grid(True, axis="y", linestyle="--", alpha=0.7)
            plt.legend(fontsize=11)
            plt.tight_layout()

            energy_plot_path = os.path.join("output", "seam_carving_energy_comparison.png")
            plt.savefig(energy_plot_path, dpi=300, bbox_inches="tight")
            plt.close()
            print(f"Energy comparison plot successfully saved to '{energy_plot_path}'")

    print(f"Runtime benchmark plot successfully saved to '{runtime_plot_path}'")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "images/sample.jpg")