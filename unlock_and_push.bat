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
git commit -m "Content: Phase 435. Phase 435 (432-Fortsetzung): Kategorien Weltgeschichte & Imperien + Webkultur & Social Media. 12 neue Modi. 4 neue JSON-Dateien (je 40 Einträge). Generatoren, i18n DE/EN/PL, timeline. verify: 163/163. MODES: 874→886. verify: 163/163."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
