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
git commit -m "Content: Phase 531. Performance: license_plates.json (3,2 MB) blockierte den Start (erste sequenzielle await-Fetch bei 18%). Jetzt nicht-blockierend nachgeladen: App startet sofort, PLATES_DATA wird per fetch().then() befuellt sobald da. Plate-Modi liefern bis dahin null (graceful, wie bei Ladefehler) und funktionieren danach. Verifiziert: vor Load null, nach Load OK. Kein blockierendes await mehr; SW-Cache unveraendert 6,1 MB.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
