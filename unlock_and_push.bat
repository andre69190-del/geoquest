@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CRITICAL FIX: Phase 165-170 — Crash fix (JSON.stringify onclick), Duplicate answers (_uOpts), Stadium/LV buttons, btn-base CSS + Menu Overhaul + Admin Dashboard + Bug Reporter"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
