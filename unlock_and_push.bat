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
git commit -m "Content: Phase 553. Empfehlungen (_forYouGames) und Daily Challenge nur noch Geo: NON_GEO_IDS-Filter in _forYouGames; DAILY_POOL_GEO (42->31) ersetzt DAILY_POOL an beiden Pick-Stellen. Haelt den Geo-Hauptbereich konsequent geo-only.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
