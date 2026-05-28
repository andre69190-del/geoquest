@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py
if errorlevel 1 (
    echo.
    echo ABORT: verify.py FAILED - fix errors before pushing!
    pause
    exit /b 1
)
echo.
git add -A
git commit -m "Content: Phase 260. Astronomie Massive Expansion: 20 Astro-Modi skaliert (+547 Einträge). astro_pin 8→35-44 Items, astro_hl 8→18-38, astro_match 10→28-58. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
