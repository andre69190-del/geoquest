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
git commit -m "Security+UX: Phase 241. syncOfflineData() cap (pendingScore<=100k, pendingCoins<=1k). Gameover: orange offline banner via pre-computed _scoreIndicator (no nested template literal). verify.py Section 0 dynamic os.listdir(data/*.json). verify: 76/76."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
