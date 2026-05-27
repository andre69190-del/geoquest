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
git commit -m "CONTENT: Phase 252. Astronomie Expansion — 17 neue Modi (4 Pin, 6 HL, 6 Match, 1 WS). MODES: 590->607. Neue Kategorien: Kontrollzentren, Teleskope, Meteoritenkrater, Dark-Sky, Raketen-Nutzlast, Missionsdauer, Gravitation, Temperaturen, Entdeckungsjahre, Exoplaneten, Sonden-Ziele, Himmelskörper-Typen, Sternbilder, Pioniere, Antriebe, Galaxientypen, WS-Schwarzes