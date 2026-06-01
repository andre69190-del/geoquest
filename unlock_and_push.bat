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
git commit -m "Content: Phase 408. UX: _exitToMenu() — nach Spielende kehrt die App zur Kategorie des gespielten Modus zurueck (11x Exit-Button ersetzt, smooth scroll, filterCat gesetzt). verify: 143/143."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
