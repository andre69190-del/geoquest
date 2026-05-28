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
git commit -m "Phase 272: SPORT_POI Full-to-50 Sprint. Alle 18 SPORT_POI_GAMES auf 50 POIs (derby, eishockey, f1, tdf, fussball, olympia u.v.m.). UEFA_STADIUMS 28->50. geo_pin Fossilien/Graeben/Rifts/Geoparks 8->30-40. hohe_stadien 9->30, leichtathletik_wm 13->19. BETA komplett aus gen.py entfernt (0x Python, 0x JS). verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
