@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 209 final — WortSchmiede 103 cities, Polish (pl) language added to 102/103 cities. All words Counter-validated across de/en/es/fr/pl."
git push origin main
pause
