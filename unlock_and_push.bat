@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX+FEAT: Phase 205 -- Wort-Schmiede (DE/EN/ES/FR city-scrabble); Fix double-comma JS SyntaxError in GEN dispatcher; Fix vercel.json: add cities_data.js to builds+routes so 30k-city data is actually served"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
