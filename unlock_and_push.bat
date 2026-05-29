@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py
if errorlevel 1 (
    echo.
    echo ABORT: verify.py FAILED - fix errors before pushing!
    pause
    exit /b 1
)
echo.
git add -A
git commit -m "Phase 281: 1v1 Sync Fix. mpCountdown render() bei jedem Tick (Countdown blieb bei 3). 11x Math.random()->rng() in Generatoren (Versus/FlagFusion/LogikGitter/TravelRoute) - gleicher Seed = gleiche Fragen fuer beide Spieler. verify: 90/90."
git push origin main