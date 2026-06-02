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
git commit -m "Content: Phase 415. Settings konsolidiert: block4+block5 zu einem EINSTELLUNGEN-Block (Design-Segmented, Sprache, Menü-Ansicht-Toggle), Sprache aus Modal entfernt, Modal heißt 'Weitere Einstellungen'. Spielübersicht: _get_type() Match/Pin-Erkennung, Konsolen/Regional-Badges, return len(rows). verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
