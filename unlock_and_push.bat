@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 223 — Karte-Sprung behoben (_mapZoom lid-gebunden, drag-vs-tap Guard, svg.node() Coords), Stadion-Dedup (Paar-LID fuer askedLids, 28 unique Pairs garantiert keine Wiederholung in 10 Fragen). Build: 1.450M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause