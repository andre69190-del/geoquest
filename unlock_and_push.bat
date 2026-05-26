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
git commit -m "FEAT: Phase 231 -- Archäologie & Verlorene Welten (60 neue Modi). 13 Pin-Modi + 12 H/L-Modi + 28 Match-Modi + 7 WS-Modi. Neue Kategorie: archaeologie. 4 JSON-Datendateien (archaeologie_*.json). MODES: 498->558. gen.py: 1.170M bytes. GeoQuest.html: 2.051M bytes. verify.py: 33/33 passed."
