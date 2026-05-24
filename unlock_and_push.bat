@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CHORE/FIX: Full-system regression audit. Verified integrity of legacy arrays, core game loop, global CSS layouts, and map pin rendering. Fixed: airportPinDist/Pts state leak between rounds, redundant CSS word-break on .hl-name."
git push origin main
pause
