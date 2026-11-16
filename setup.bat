@echo off
REM ============================================================
REM  Seam Carving project - setup for Windows
REM  Skips anything that's already installed.
REM  Just double-click this file, or run: setup.bat
REM ============================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/5] Checking Python (need 3.9 or newer)...
set "PY="
REM Try the "py" launcher first (handles multiple versions), then "python".
REM The version check also filters out the fake Microsoft Store "python" alias.
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>nul && set "PY=python"
)
if defined PY (
    for /f "delims=" %%v in ('%PY% --version') do echo   [OK]   %%v already installed - skipping install
) else (
    echo   [..]   No Python 3.9+ found. Installing Python 3.12 with winget...
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    echo.
    echo   Python installed. CLOSE this window and run setup.bat again
    echo   so Windows picks up the new PATH.
    pause
    exit /b 0
)

echo.
echo [2/5] Checking Git...
where git >nul 2>nul
if errorlevel 1 (
    echo   [..]   Git not found. Installing Git with winget...
    winget install -e --id Git.Git --accept-source-agreements --accept-package-agreements
    echo.
    echo   Git installed. CLOSE this window and run setup.bat again.
    pause
    exit /b 0
)
for /f "delims=" %%v in ('git --version') do echo   [OK]   %%v already installed - skipping

echo.
echo [3/5] Checking virtual environment...
if exist ".venv\Scripts\python.exe" (
    echo   [OK]   .venv already exists - skipping creation
) else (
    %PY% -m venv .venv
    if errorlevel 1 (
        echo   [FAIL] Could not create virtual environment.
        pause
        exit /b 1
    )
    echo   [OK]   Created .venv
)

echo.
echo [4/5] Installing / updating libraries...
".venv\Scripts\python.exe" -m pip install --upgrade pip -q
".venv\Scripts\python.exe" -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo   [FAIL] pip install failed - check the error above.
    pause
    exit /b 1
)
echo   [OK]   Libraries installed / up to date

echo.
echo [5/5] Checking git repository...
if exist ".git" (
    echo   [OK]   Git repo already exists - skipping
) else (
    git init -b main
    git add .
    git commit -m "Initial project scaffold" || echo   [..]   Commit skipped - set git user.name / user.email first
)

echo.
echo ============================================================
echo  DONE!
echo    Activate:  .venv\Scripts\activate
echo    Tests:     pytest
echo    App:       streamlit run app.py
echo ============================================================
pause
