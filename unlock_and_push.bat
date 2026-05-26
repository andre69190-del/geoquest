@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 226 — Karten-Zoom-Reset in lq() (Grand Canyon zeigte Australien), drawWorldMap Zoom-Handler nur im interaktiven Modus (Feedback-Animation ueberschrieb _mapZoom=null), Suche-Fix, HL-Deutsch, Sunrise-Fenster, Streak-Pill. Build: 1.451M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause