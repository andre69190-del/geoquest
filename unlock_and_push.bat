@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT/FIX: Phase 212 Metagame Audit — category+game selector for Live 1vs1 and Hot-Seat modes, seed leak fix, mpGameCh memory leak fix, mpGameSec missing backtick syntax fix."
git push origin main
pause
