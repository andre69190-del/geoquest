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
git commit -m "Content: Phase 406. Phase 406: Bugfixes — Spoiler genGamesPinQ, games_match_kategorie immer null (fixedPool 3->4), catLabels games, hl_games_dev_lat Syntax; JS 143/143. verify: 143/143."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
