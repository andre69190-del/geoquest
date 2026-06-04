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
git commit -m "Content: Phase 479. verify.py erweitert (Check 20: undefinierte/ungeschuetzte *_DATA-Referenzen -> faengt Runtime-Crash-Klasse aus Phase 478 ab, jetzt 192/192) + grosses 9-Dimensionen-Audit nach Umbau 467-478. Ergebnis: alle Dimensionen gruen, keine offenen kritischen/mittleren Punkte. Bericht in PHASE479_AUDIT.md. Beobachtungen (niedrig): i18n-Schuld im Einstellungs-Modal (vorbestehend), home_hi-Namensumbruch kosmetisch.. verify: 192/192."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
