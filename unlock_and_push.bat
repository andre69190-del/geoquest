@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "Phase 191: Fix #mainGamesGrid wrongly grid-ified by nuclear CSS - now block, accordion-content gets grid"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
