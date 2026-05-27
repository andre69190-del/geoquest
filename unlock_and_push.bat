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
git commit -m "PWA: Phase 238. SW upgrade: blob→external sw.js. Hash-versioned cache (geoquest-<hash>). All 24 data/*.json in ASSETS. Promise.allSettled install. manifest.json synced (theme=#10b981, SVG icon). verify: 56/56."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
