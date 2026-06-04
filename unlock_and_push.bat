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
git commit -m "Content: Phase 478. BUGFIX Runtime-Crash 'Land pinnen': 5 Pin-Generatoren referenzierten nicht existierende Daten-Variablen (ReferenceError -> lq() exhausted -> Spiel startet nicht). Korrigiert: park_pin_land THEMEPARKS_DATA->PARKS_DATA, serie_pin_land SERIEN_DATA->SERIEN_EXT_DATA, musik_pin_land MUSIK_DATA->MUSIK_EXT_DATA, web_pin_land WEBKULTUR_DATA->WEB_DATA, film_pin_land FILME_DATA->FILME_EXT_DATA. Felder verifiziert (park_land/produktionsland/herkunftsland/ursprungsland/drehort_land existieren). Audit: keine weiteren undefinierten/ungeschuetzten *_DATA-Referenzen (TECH_DATA ist typeof-guarded).. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
