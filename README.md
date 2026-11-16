# Seam Carving – Algorithm Analysis Assignment 2

Content-aware image resizing using Dynamic Programming, Greedy and Graph Cut.

## Quick start
**Windows:** double-click `run.bat`. **Ubuntu / macOS:** `bash run.sh`.
The first run installs everything automatically; after that you get a menu (app / tests / benchmark).

## Setup (manual)
Needs **Python 3.9 or newer**. The scripts detect what you already have and skip anything that's installed.

| OS | Run |
|---|---|
| Windows | double-click `setup.bat` |
| Ubuntu (any version) / WSL / macOS | `bash setup.sh` |

```
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Ubuntu / macOS
pytest                 # run tests (unfinished parts show as "skipped")
streamlit run app.py   # interactive demo
python benchmark.py images\sample.jpg
```

## Who owns what
| File | Owner | Job |
|---|---|---|
| `seamcarve/energy.py`, `seamcarve/carve.py` | Person 1 | Energy map, seam removal, transpose, resize loop |
| `seamcarve/dp.py` | Person 2 | DP seam finder |
| `seamcarve/greedy.py` | Person 3 | Greedy seam finder |
| `seamcarve/graphcut.py` | Person 4 | Min-cut / max-flow seam finder |
| `tests/`, `benchmark.py` | Person 5 | Testing, timing, charts |
| `app.py`, `.github/workflows/ci.yml` | Person 6 | Streamlit app, visualisation, CI |

## Shared contract
- Energy: `compute_energy(img) -> H x W float array`
- Every seam finder: `find_seam_xxx(energy) -> length-H int array` (`seam[i]` = column in row i)
- `remove_seam(img, seam) -> image one column narrower`

## Git workflow
```
git checkout -b person1-energy     # your own branch
git add . && git commit -m "..."
git push -u origin person1-energy  # then open a Pull Request on GitHub
```
Always `git pull origin main` before starting work.
