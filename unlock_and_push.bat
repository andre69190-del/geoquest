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
git commit -m "Content: Phase 535. Fehler-Tagebuch + Pin-Tipp-Anzeige. (1) renderSrsListModal: Modal listet alle gq_srs-Eintraege (Frage -> richtige Antwort + Box-Punkte), Zugang via Tagebuch-Button in der SRS-Home-Card, mit 'Schwaechen ueben'-Shortcut. (2) Pin-Modus: Klickkoordinaten in S.lastPinLat/Lng gespeichert; im readOnly-Karten-Render wird der eigene Tipp (roter Marker) + Verbindungslinie zur richtigen Lage gezeichnet. i18n DE/EN/PL. Verifiziert: Tagebuch listet korrekt, Pin-Code im Build.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
