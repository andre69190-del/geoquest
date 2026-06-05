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
git commit -m "Content: Phase 517. Options-Qualitaet: 4 Jahr-MC-Generatoren (auto/games/hw baujahr, games peak_year) + subway erzeugten doppelte Optionen (z.B. 1999/1999, subway sogar Antwort 12 doppelt), weil Distraktor-Pools nicht dedupliziert wurden. Fix: Pools per Set deduplizieren und Antwort ausschliessen. Neuer Dauertest option_quality_test.js (5. Ebene) findet doppelte/Einzel-Optionen ueber alle MC-Modi. Ergebnis: 0 DUP, 0 SINGLE.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
