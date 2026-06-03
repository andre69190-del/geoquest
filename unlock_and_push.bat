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
git commit -m "Content: Phase 461. Home-Hero-Layout: Live 1vs1 Duell + Lokal Hot-Seat als kompaktes Paar nebeneinander (je halbe Breite, vertikale Karten: Icon/Label/Button, Untertitel entfernt). Daily Challenge bleibt voll breit als Haupt-Hero. Spart Banner-Hoehe -> Empfehlungen rutschen nach oben. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
