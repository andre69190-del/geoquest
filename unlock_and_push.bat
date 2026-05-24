@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: 3 JS SyntaxErrors -- double-comma in GEN dispatcher; Phase 204 generator functions inside object literal (moved before const GEN); Wort-Schmiede escaped-quote bugs in single-quoted strings; Fix vercel.json cities_data.js missing from builds+routes"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
