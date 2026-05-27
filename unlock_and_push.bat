@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py || (echo. && echo [ABORT] verify.py FAILED - fix errors before pushing! && pause && exit /b 1)
echo.
git add -A
git commit -m "DATA: Phase 243. 3 Neue Welten: Astronomie (astro_pin/hl/match/ws), Geologie (geo_pin/hl/match/ws), Sport-Wissen (sport_pin/hl/match/ws). 12 JSON files, 32 new modes, 3 new MODE_CATS. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
