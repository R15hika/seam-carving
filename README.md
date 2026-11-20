# Seam Carving – Algorithm Analysis Assignment 2

Content-aware image resizing using Dynamic Programming, Greedy and Graph Cut.

## Quick start
| OS                                 | Run                    |
|------------------------------------|------------------------|
| Windows                            | double-click `run.bat` |
| Ubuntu (any version) / WSL / macOS | `bash run.sh`          |

It installs anything missing (needs Python 3.9+, skips whatever you already have), then shows a menu to open the app, run tests or run the benchmark.

Running things by hand instead:
```
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Ubuntu / macOS
pytest  # run tests (unfinished parts show as "skipped")
streamlit run app.py  # interactive demo
python benchmark.py images/sample.jpg  # timing benchmark
```

## Who owns what
| File                                        | Owner                   | Job                                              |
|---------------------------------------------|-------------------------|--------------------------------------------------|
| `seamcarve/energy.py`, `seamcarve/carve.py` | Rishika Bimal Attodi    | Energy map, seam removal, transpose, resize loop |
| `seamcarve/dp.py`                           | Sim Kah Yan             | DP seam finder                                   |
| `seamcarve/greedy.py`                       | Soo Ke Yee              | Greedy seam finder                               |
| `seamcarve/graphcut.py`                     | Nurafifah Binte Jasmani | Min-cut / max-flow seam finder                   |
| `tests/`, `benchmark.py`                    | Chang Qi Xuan Celest    | Testing, timing, charts                          |
| `app.py`, `.github/workflows/ci.yml`        | Ang Yu Xuan             | Streamlit app, visualisation, CI                 |

## Shared contract
- Energy: `compute_energy(img) -> H x W float array`
- Every seam finder: `find_seam_xxx(energy) -> length-H int array` (`seam[i]` = column in row i)
- `remove_seam(img, seam) -> image one column narrower`

## Git workflow
```
git checkout -b person1-energy  # your own branch
git add . && git commit -m "..."
git push -u origin person1-energy  # then open a Pull Request on GitHub
```
Always `git pull origin main` before starting work.
