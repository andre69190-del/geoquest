@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 221 — Offline-Modus (SW gq-v10, network-first Cache), Wort-Schmiede Multilingual-Bonus (+10 Pkt wenn DE+EN gueltig), Sonnen-Kompass neuer Modus (40 Staedte, Sonnenuntergangs-Azimut nach Spencer-Formel, NW/W/SW). Build: 1.447M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause