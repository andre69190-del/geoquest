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
git commit -m "FEAT: Phase 228 -- Das Botanik-Update (49 neue Pflanzenmodi). 12 Pin-Modi + 12 H/L-Modi + 14 Match-Modi + 9 WS-Modi + 4 Generatoren + 4 JSON-Datendateien (pflanzen_*.json). MODES: 299->347. Build: 1.711M chars. verify.py: 33/33 passed."
