@echo off
REM seam carving - double-click to install anything missing and run the project
setlocal
cd /d "%~dp0"

echo Checking Python (need 3.9 or newer)...
set "PY="
REM try the py launcher first, then python, the version check also skips the fake microsoft store python
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>nul && set "PY=python"
)
if defined PY (
    for /f "delims=" %%v in ('%PY% --version') do echo   [OK] %%v already installed
) else (
    echo   No Python 3.9+ found, installing Python 3.12 with winget...
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    echo.
    echo   Python installed. Close this window and double-click run.bat again
    pause
    exit /b 0
)

REM OneDrive syncing can corrupt the .venv (half-synced numpy/opencv files), so warn about it
echo "%~dp0" | find /i "OneDrive" >nul && (
    echo   [WARN] this folder is inside OneDrive, which can break installed libraries.
    echo          If you get import errors, move the project somewhere like C:\Projects
)

REM if the venv's python itself is broken (python upgraded/uninstalled, venv copied from another PC), rebuild it
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys" >nul 2>nul || (
        echo   .venv is broken, rebuilding it...
        rmdir /s /q .venv
    )
)

if exist ".venv\Scripts\python.exe" (
    echo   [OK] .venv already exists
) else (
    echo Creating virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo   [FAIL] couldn't create the virtual environment
        pause
        exit /b 1
    )
)
set "VPY=.venv\Scripts\python.exe"

set "CHECK=import numpy, cv2, matplotlib, streamlit, pytest"

REM install when requirements.txt changed, and also actually import everything,
REM because a library can be "installed" but broken (e.g. numpy missing its compiled files)
fc /b requirements.txt .venv\installed-requirements.txt >nul 2>nul || goto install
"%VPY%" -c "%CHECK%" >nul 2>nul || goto repair
goto libs_ok

:install
echo Installing libraries, first time takes a minute...
"%VPY%" -m pip install --upgrade pip -q
"%VPY%" -m pip install -r requirements.txt -q
if errorlevel 1 goto pipfail
"%VPY%" -c "%CHECK%" >nul 2>nul && goto libs_done

:repair
echo   Some libraries are broken, reinstalling them (takes a minute)...
"%VPY%" -m pip install --force-reinstall --no-cache-dir -r requirements.txt -q
if errorlevel 1 goto pipfail
"%VPY%" -c "%CHECK%"
if errorlevel 1 (
    echo   [FAIL] libraries still won't import, see the error above.
    echo          Delete the .venv folder and run run.bat again.
    echo          If the project is inside OneDrive, move it out first.
    pause
    exit /b 1
)

:libs_done
copy /y requirements.txt .venv\installed-requirements.txt >nul
:libs_ok
echo   [OK] libraries up to date
goto menu

:pipfail
echo   [FAIL] pip install failed, check the error above
pause
exit /b 1

:menu
echo.
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
REM app gets its own window so this menu stays usable, close that window to stop the app
start "Seam Carving App" "%VPY%" -m streamlit run app.py
REM opens the browser a few seconds later once the server is up
start "" /min powershell -NoProfile -Command "Start-Sleep 3; Start-Process 'http://localhost:8501'"
echo App started in a separate window, close that window to stop it
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
start "Seam Carving" cmd /k ".venv\Scripts\activate.bat"
goto menu
