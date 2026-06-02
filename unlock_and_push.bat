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
git commit -m "Content: Phase 434. Phase 434: Datenbasis-Upgrade. generate_spieluebersicht.py: 3 neue Fn-Mappings (0 Warnings). literatur_extended 40→80, robotik_extended 40→80. timeline.json: robot_jahr auf 80 Einträge. verify: 160/160. verify: 160/160."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
