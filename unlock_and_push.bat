@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 225 — Suche repariert (inline display:none blockierte .open, removeProperty fix), Kuestenlaenge Mojibake, HL-Modi Deutsch, Sunrise 15-75deg Fenster, Streak-Pill kleiner, Karte-Sprung, Stadion-Dedup. Build: 1.451M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause