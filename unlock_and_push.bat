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
git commit -m "Content: Phase 556. Geo-Hauptbereich konsequent: 'Zuletzt gespielt'-Leiste nach Ansicht gefiltert (Geo zeigt nur Geo, Allgemeinwissen nur Nicht-Geo); Kategorie-Empfehlungen (_forYouCats/_forYouGames) nur geo-reiche Kategorien (_catGeoRich: geo>=1/3) -> kein 'Games & Hardware' mehr im Geo-Bereich. Hin/Zurueck-Buttons + Labels verifiziert.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
