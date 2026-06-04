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
git commit -m "Content: Phase 484. Generator-Rauchtest (smoke_test.js): laedt GeoQuest.html in Node-VM mit Browser-Stubs, ruft jeden GEN-Modus 6x auf, meldet THROW (Crash) und persistentes NULL. Fand+fixte hl_river (genHLRiverQ: lokale 'const RIVERS_REAL=_rvPool' ueberschattete die globale -> TDZ-Crash; lokalen Schatten entfernt, _rvPool genutzt). Ergebnis: 998 getestet, 859 OK, 0 THROW, 120 ws_null (erwartet), 19 NULL (brauchen Live-Daten/Spielzustand - zur Sichtung). verify 193/193.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
