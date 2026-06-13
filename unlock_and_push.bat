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
git commit -m "Content: Phase 552. Allgemeinwissen-Split: Hauptbereich zeigt nur noch Geo-Spiele, neuer Button 'Allgemeinwissen' (Banner ueber Empfehlungen) schaltet auf Nicht-Geo-Ansicht (Kategorien bleiben erhalten, gefiltert). Umkehrbar per Filter (NON_GEO_IDS, 545 IDs aus Geo-Audit) - nichts geloescht. Geo-Heroes/Empfehlungen nur in Geo-Ansicht. Album-Oeffnen-Button ~1/3 kleiner. i18n DE/EN/PL.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
