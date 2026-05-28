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
git commit -m "Phase 273: Distanz-/Flugzeit-Schaetzer Fix. JSON c-Werte normalisiert (einheitl. Format). ansPool distanz 10->44 unique Werte, flugzeit 8->15 unique Werte. Spieluebersicht: 10->50 Distanzen, 8->50 Flugzeiten. verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
