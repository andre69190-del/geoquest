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
git commit -m "Content: Phase 530. Barrierefreiheit: 7 Flaggen-<img> ohne alt -> alt='Flagge' ergaenzt (0 verbleibend). aria-label fuer Icon-only-Buttons: HUD (Vorlesen/Feedback/Beenden/Einstellungen, 27x) + Loeschen/Bestaetigen/Aktualisieren/Schliessen (7x). Neuer Dauertest a11y_check.py (9. Ebene): FAIL bei <img> ohne alt, WARN bei Icon-only-Buttons ohne Label. Ergebnis 0 FAIL, 69->3 WARN.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
