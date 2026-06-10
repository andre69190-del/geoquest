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
git commit -m "Content: Phase 545. Einstellungen: SRS an/aus-Schalter ('Fehler merken') im Settings-Modal. gq_srs_off=1 -> _srsAdd erfasst keine Fehler mehr; _srsToggle schaltet um. Schwierigkeit persistiert bereits via gq_diffx (bestaetigt). i18n Fehler merken/An/Aus DE/EN/PL. Verifiziert: an erfasst, aus blockt, wieder an erfasst.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
