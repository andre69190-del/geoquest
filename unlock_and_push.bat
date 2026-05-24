@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: 50/50 joker dynamic guard -- _is2ans now checks opts.length<=2 not hardcoded types; useFiveO() blocks with toast for binary modes; covers all Phase 204 binary games (Hauptstadt-Distanz, Insel/Festland, Flugrouten-Duell, Aequator etc)"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
