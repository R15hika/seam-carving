#!/usr/bin/env bash
# ============================================================
#  Seam Carving project - setup for Linux (any Ubuntu) / macOS / WSL
#  Skips anything that's already installed.
#  Run with:   bash setup.sh
# ============================================================
set -e
cd "$(dirname "$0")"

MIN_MAJOR=3
MIN_MINOR=9

ok()   { echo "  [OK]   $*"; }
info() { echo "  [..]   $*"; }
fail() { echo "  [FAIL] $*"; exit 1; }

have() { command -v "$1" >/dev/null 2>&1; }

# Returns 0 if the given python is >= 3.9
version_ok() {
    "$1" -c "import sys; sys.exit(0 if sys.version_info >= ($MIN_MAJOR, $MIN_MINOR) else 1)" 2>/dev/null
}

# Find the newest suitable python already on the machine
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
        # Newer Ubuntu (22.04+) ships Python >= 3.10 - just install the default
        sudo apt-get install -y python3 python3-venv python3-pip
        if ! find_python >/dev/null; then
            # Older Ubuntu (e.g. 20.04 = Python 3.8): get 3.11 from deadsnakes PPA
            info "Default Python is too old, installing Python 3.11 from deadsnakes PPA..."
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.11 python3.11-venv
        fi
    elif have brew; then
        brew install python@3.12
    else
        fail "Couldn't auto-install Python. Install Python 3.9+ from https://www.python.org and re-run."
    fi
}

echo
echo "[1/5] Checking Python (need $MIN_MAJOR.$MIN_MINOR or newer)..."
if PY=$(find_python); then
    ok "$($PY --version) already installed ($PY) - skipping install"
else
    info "No Python $MIN_MAJOR.$MIN_MINOR+ found, installing..."
    install_python
    PY=$(find_python) || fail "Python install failed."
    ok "Installed $($PY --version)"
fi

echo
echo "[2/5] Checking venv support..."
if "$PY" -m venv --help >/dev/null 2>&1 && "$PY" -c "import ensurepip" 2>/dev/null; then
    ok "venv already available - skipping"
else
    # Ubuntu splits venv into a separate package, e.g. python3.12-venv
    VER=$("$PY" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if have apt-get; then
        info "Installing python$VER-venv..."
        sudo apt-get install -y "python$VER-venv" || sudo apt-get install -y python3-venv
        ok "venv installed"
    else
        fail "venv module missing for $PY - please install it and re-run."
    fi
fi

echo
echo "[3/5] Checking Git..."
if have git; then
    ok "$(git --version) already installed - skipping"
else
    info "Installing git..."
    if have apt-get; then sudo apt-get install -y git
    elif have brew; then brew install git
    else fail "Install git from https://git-scm.com and re-run."
    fi
    ok "$(git --version) installed"
fi

echo
echo "[4/5] Setting up virtual environment + libraries..."
if [ -x ".venv/bin/python" ]; then
    ok ".venv already exists - skipping creation"
else
    "$PY" -m venv .venv
    ok "Created .venv"
fi
.venv/bin/python -m pip install --upgrade pip -q
.venv/bin/python -m pip install -r requirements.txt -q
ok "Libraries installed / up to date"

echo
echo "[5/5] Checking git repository..."
if [ -d ".git" ]; then
    ok "Git repo already exists - skipping"
else
    git init -b main 2>/dev/null || { git init; git checkout -b main; }
    git add .
    git commit -m "Initial project scaffold" || info "Commit skipped (set git user.name/user.email first)"
    ok "Git repo initialised"
fi

echo
echo "============================================================"
echo " DONE!"
echo "   Activate:  source .venv/bin/activate"
echo "   Tests:     pytest"
echo "   App:       streamlit run app.py"
echo "============================================================"
