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
git commit -m "Content: Phase 411. Games & Hardware: 30 Konsolen (Atari bis PS5), Kategorie umbenannt, 6 neue Modi (Timeline, 2x H/L Verkauf+Preis, 3x Match Hersteller/Medium/Handheld). verify: 145/145."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
