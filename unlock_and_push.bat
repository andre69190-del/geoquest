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
git commit -m "Content: Phase 329. Auto-Quartett: 4 HL-Modi (PS, vmax, accel, ccm) aus data/autos.json — 50 Fahrzeuge von VW Käfer bis Rimac Nevera, 17 Länder, EVs im ccm-Array ausgeschlossen. verify: 139/139."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
