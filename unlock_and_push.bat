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
git commit -m "ENGINE+DATA: Phase 242. Tiere-Pin: tiere_pin.json (10 categories) via TIER_PIN_DATA + Object.assign(KULTUR_DATA). Daily rotation: 5-mode pool (city/flag/wahrzeichen/getraenke/tiere_endemisch). Blitz mode: 60s speed round, no feedback, flash border, gameover on timeout. verify: 77/77."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
