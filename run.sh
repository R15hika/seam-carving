#!/usr/bin/env bash
# ============================================================
#  Seam Carving - run with:  bash run.sh
#  First time: runs setup.sh automatically.
# ============================================================
cd "$(dirname "$0")"

if [ ! -x ".venv/bin/python" ]; then
    echo "First run detected - running setup first..."
    bash setup.sh || exit 1
fi

VPY=.venv/bin/python

while true; do
    echo
    echo "============================================"
    echo "   Seam Carving"
    echo "============================================"
    echo "   1. Open the app (in your browser)"
    echo "   2. Run tests"
    echo "   3. Run benchmark"
    echo "   4. Quit"
    echo "============================================"
    read -rp "Pick 1-4: " choice
    case "$choice" in
        1) "$VPY" -m streamlit run app.py ;;
        2) "$VPY" -m pytest -v ;;
        3) read -rp "Image path: " img; [ -n "$img" ] && "$VPY" benchmark.py "$img" ;;
        4) exit 0 ;;
    esac
done
