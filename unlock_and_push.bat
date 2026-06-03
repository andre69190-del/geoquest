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
git commit -m "Content: Phase 463. Eltern-PIN: Kinder-Modus mit 4-stelligem PIN sicherbar. _toggleKidsMode fragt beim Ausschalten den PIN ab (renderPinModal, _pinSubmit/_pinRemove, gq_kids_pin). Setzen/Aendern/Entfernen im Einstellungs-Modal. Kinder koennen den Kinder-Modus nicht mehr selbst abschalten. i18n DE/EN/PL. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
