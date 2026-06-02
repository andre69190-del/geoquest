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
git commit -m "Content: Phase 423. 8 neue Modi aus ungenutzten Datenfeldern: hl_konsolen_erscheinungsjahr/eingestellt, konsolen_match_spiel/aufloesung, hl_auto_nordschleife/baujahr_ende, games_match_publisher_land, hl_games_publisher_lng. MODES 802->810. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
