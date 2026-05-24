@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Post-audit hotfixes — uk_pin map render branch, uk_hl_prompt i18n key, MODE_CATS.lifestyle registration of all 27 uk_* modes."
git push origin main
pause
