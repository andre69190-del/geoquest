@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: CITIES lat/lng missing -- all Phase 204 generators returned null because cities_slim had no coordinates; add lat/lng to cities_slim; hauptstadt_distanz: match capitals by cc not country name string (US vs USA mismatch); Phase 206 audit hardening"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
