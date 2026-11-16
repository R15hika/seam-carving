#!/usr/bin/env bash
# seam carving - run with: bash run.sh
# installs anything missing (any ubuntu version, wsl or macos) then shows the menu
cd "$(dirname "$0")"

have() { command -v "$1" >/dev/null 2>&1; }

version_ok() {
    "$1" -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" 2>/dev/null
}

# newest python 3.9+ already on the machine
find_python() {
    for p in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
        if have "$p" && version_ok "$p"; then
            echo "$p"; return 0
        fi
    done
    return 1
}

install_python() {
    if have apt-get; then
        sudo apt-get update
        # ubuntu 22.04+ already ships 3.10 or newer
        sudo apt-get install -y python3 python3-venv python3-pip
        if ! find_python >/dev/null; then
            # older ubuntu like 20.04 only has 3.8, so grab 3.11 from deadsnakes
            echo "  default python is too old, installing 3.11 from deadsnakes..."
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.11 python3.11-venv
        fi
    elif have brew; then
        brew install python@3.12
    else
        echo "  [FAIL] couldn't install python, get 3.9+ from python.org and run this again"
        exit 1
    fi
}

echo "Checking Python (need 3.9 or newer)..."
if PY=$(find_python); then
    echo "  [OK] $($PY --version) already installed"
else
    echo "  no python 3.9+ found, installing..."
    install_python
    PY=$(find_python) || { echo "  [FAIL] python install failed"; exit 1; }
fi

if [ -x ".venv/bin/python" ]; then
    echo "  [OK] .venv already exists"
else
    # ubuntu splits venv into its own package, like python3.12-venv
    if ! "$PY" -c "import ensurepip" 2>/dev/null; then
        VER=$("$PY" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if have apt-get; then
            echo "  installing python$VER-venv..."
            sudo apt-get install -y "python$VER-venv" || sudo apt-get install -y python3-venv
        else
            echo "  [FAIL] venv module missing for $PY"; exit 1
        fi
    fi
    echo "Creating virtual environment..."
    "$PY" -m venv .venv || { echo "  [FAIL] couldn't create .venv"; exit 1; }
fi
VPY=.venv/bin/python

# only reinstall libraries when requirements.txt has changed since last time
if ! cmp -s requirements.txt .venv/installed-requirements.txt; then
    echo "Installing libraries, first time takes a minute..."
    "$VPY" -m pip install --upgrade pip -q
    "$VPY" -m pip install -r requirements.txt -q || { echo "  [FAIL] pip install failed"; exit 1; }
    cp requirements.txt .venv/installed-requirements.txt
fi
echo "  [OK] libraries up to date"

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
        1)
            # opens the browser once the server is up
            (sleep 3; xdg-open http://localhost:8501 2>/dev/null || open http://localhost:8501 2>/dev/null) &
            "$VPY" -m streamlit run app.py ;;
        2) "$VPY" -m pytest -v ;;
        3) read -rp "Image path: " img; [ -n "$img" ] && "$VPY" benchmark.py "$img" ;;
        4) exit 0 ;;
    esac
done
