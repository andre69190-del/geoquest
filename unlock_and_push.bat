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
git commit -m "Content: Phase 537. ingame_render_test deckt jetzt SRS-Replay ab: ~25 falsch-Snapshots werden gespeichert und im Review-Modus (S.srsRun) gerendert (25 OK, 0 Fehler), plus renderSrsHero/renderSrsListModal/renderDailyHero. fail-Zaehler integriert.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
