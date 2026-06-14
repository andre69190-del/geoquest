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
git commit -m "Content: Phase 571. Spielstand Export/Import (Schulen/Offline): Einstellungen -> 'Spielstand sichern' (alle gq_/geoquest_-Keys als geoquest-spielstand.json herunterladen) + 'Spielstand laden' (JSON einlesen, Keys zuruckschreiben, reload). Kein Cloud-Konto noetig - ideal fuer Kiosk-Modus, der localStorage loescht. i18n DE/EN/PL.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
