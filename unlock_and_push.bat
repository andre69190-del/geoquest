@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "Phase 183: Filter chips window.filterByCategory, display-name mapping, post-render setTimeout"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
