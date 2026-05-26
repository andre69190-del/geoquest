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
git commit -m "FIX+FEAT: Phase 228-231 + Bugfixes + Polish WS + Refactoring. Tiere/Pflanzen in separate Kategorien aufgeteilt. Phase 229: Gastronomie (45 Modi). Phase 230: Tech & E-Mob (2 Kategorien, ~90 Modi). Phase 231: Archaeologie (60 Modi). BUGFIX: genUniversalPinQ fuer {prompt,items}-Format (6 Tiere-Modi hingen). Polish WS: 4680 polnische Woerter zu 54 WS-Eintraegen hinzugefuegt. Refactoring: 16 doppelte Generatoren durch 4 Factory-Funktionen ersetzt. MODES: 558->692. GeoQuest.html: 2.180M. verify.py: 53/53 passed."
