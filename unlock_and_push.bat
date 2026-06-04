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
git commit -m "Content: Phase 506. MODE_CATS-Fix: alle 84 neuen Modi aus Phasen 498-505 in ihre jeweiligen Kategorien eingetragen (astronomie, autos, boardgames, capitals, eu_plates, fluesse, games, hunde, klima, map_mode, nparks, ozeane, pflanzen, pure_geo, sport, themeparks, tiere, zuege). Ohne diesen Fix waren die neuen Spiele im Kategorie-Grid unsichtbar. verify 193/193 ✓. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
