@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 224 — Kuestenlaenge Mojibake, HL-Modi auf Deutsch (higher/lower), Sunrise 15-75deg Fenster (kein Manchester vs Philippinen mehr), Streak-Pill kleiner (RUNDE sichtbar), Karte-Sprung (_mapZoom lid-gebunden), Stadion-Dedup (28 unique Pairs). Build: 1.451M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause