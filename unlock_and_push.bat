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
git commit -m "Content: Phase 557. Banner ueberarbeitet: Ueberschrift = aktueller Bereich, Button = anderer Bereich. Geo-Ansicht: 'GeoQuest / Spiele mit Geo-Bezug' + Button 'Allgemeinwissen ›'. Allgemeinwissen: 'Allgemeinwissen / Spiele ohne Geo-Bezug' + Button '‹ GeoQuest'. Kein doppeldeutiges 'Allgemeinwissen' mehr.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
