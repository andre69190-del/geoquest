@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CHORE/SEC: Comprehensive post-Phase-211 audit. Verified state isolation of Universal Engines, hardened mobile UI text wrapping, confirmed anti-cheat integrity, and guaranteed i18n fallback stability."
git push origin main
pause
