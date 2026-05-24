@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 214 Silent-Fail Bugfix. Fixed Alphabet-Sprint crash (distractors null-excludeFn TypeError), added toast for unavailable modes, marked Logik-Gitter/Reiseroute/SLF as coming-soon, enlarged mobile tap targets for info/fav buttons."
git push origin main
pause
