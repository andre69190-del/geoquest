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
git commit -m "Content: Phase 360. Gaming-Kategorie: 50 Spiele (30 Modern/Mobile + 20 Klassiker), 13 Modi (games_pin, genre/land/adaption-Match, H/L release/vk/metacritic/usk, Baujahr-MC). Bridge: dev_lat/dev_lng → echter GeoQuest-Pin-Modus.. verify: 141/141."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
