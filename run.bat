@echo off
REM ============================================================
REM  Seam Carving - double-click to run.
REM  First time: runs setup.bat automatically.
REM ============================================================
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo First run detected - running setup first...
    call setup.bat
    if not exist ".venv\Scripts\python.exe" (
        echo Setup didn't finish. If it installed Python or Git, just double-click run.bat again.
        pause
        exit /b 1
    )
)

set "VPY=.venv\Scripts\python.exe"

:menu
cls
echo ============================================
echo    Seam Carving
echo ============================================
echo    1. Open the app (in your browser)
echo    2. Run tests
echo    3. Run benchmark
echo    4. Open a terminal with the environment ready
echo    5. Quit
echo ============================================
set "choice="
set /p "choice=Pick 1-5: "

if "%choice%"=="1" goto app
if "%choice%"=="2" goto tests
if "%choice%"=="3" goto bench
if "%choice%"=="4" goto shell
if "%choice%"=="5" exit /b 0
goto menu

:app
echo Starting app... (close this window or press Ctrl+C to stop it)
"%VPY%" -m streamlit run app.py
pause
goto menu

:tests
"%VPY%" -m pytest -v
pause
goto menu

:bench
set "img="
set /p "img=Image path (drag a picture into this window, then press Enter): "
if not defined img goto menu
"%VPY%" benchmark.py %img%
pause
goto menu

:shell
REM Opens a new cmd window with the venv activated
start "Seam Carving" cmd /k ".venv\Scripts\activate.bat"
goto menu
