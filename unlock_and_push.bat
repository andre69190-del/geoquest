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
git commit -m "Phase 271-275: Full-to-50 Sprint + SPORT_POI + Schaetzer-Fix + Anti-Spoiler + Map-Scroll-Fix. SPORT_POI 18x50, UEFA 50, geo_pin gefuellt, BETA entfernt. Distanz/Flugzeit-Pools normalisiert. _mkPinQ ohne Stadtname. Pin-Map translateExtent enger + Reset-Button. verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
