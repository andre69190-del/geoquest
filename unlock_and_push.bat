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
git commit -m "Content: Phase 405. Batch 3: 20 Indie/Klassiker-Spiele + peak_year + publisher_lat/lng + 3 neue Modi (peak_year_mc, hl_peak_year, hl_publisher_lat) + validate_content Indie-Enum. verify: 143/143."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
