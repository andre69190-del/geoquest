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
git commit -m "Content: Phase 559. Verbesserungen: 'Zufall' (playRandomGame) respektiert Geo/Allgemeinwissen-Split; 19 alte gen.py-Backups entfernt; Session-Starter Doku-Note zum Geo-Split (NON_GEO_IDS); Spieluebersicht-Generator nach Bereichen GeoQuest(549)/Allgemeinwissen(545) getrennt + Hero-Zaehler.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
