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
git commit -m "Content: Phase 450. UX: Fortschritt-sichern-Button aus Gast-Header entfernt, stattdessen 👤-Login-Icon in Header-Iconreihe. 7 i18n-Keys (home_login_btn) in allen Sprachen.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
