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
git commit -m "Phases 278-280: Data Push-to-80 + Mobile Fixes + Critical Bugfixes. SPORT_POI 12x50->80, UEFA 50->80. iOS PWA install, Landscape 350ms+resize. lid-Fix (match/crest/jersey/stadium), rng()-Sync, 1v1 opts-guard, Crests 10->51. verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
