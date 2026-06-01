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
git commit -m "Content: Phase 354. UX: Feedback-Anzeigedauer +1,5 s — Einzel: 1900→3400 ms, IATA: 2800→4300 ms, startNextRound: 1500→3000 ms (5×). Multiplayer (5500 ms) unverändert.. verify: 140/140."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
