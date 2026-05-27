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
git commit -m "UX: Phase 238-239. SW: blob→sw.js, hash-versioned cache, 24 data files, Promise.allSettled. manifest synced. Auth: navigator.onLine guard (4 funcs), _authErrMsg() helper, {} crash fix. verify: 56/56."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
