@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CHORE/FIX: Post-expansion audit. Fixed JSON syntax/formatting, hardened CSS for long word wrapping, and ensured pristine state resets for Wort-Schmiede levels."
git push origin main
pause
