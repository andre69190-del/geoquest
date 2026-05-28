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
git commit -m "Phase 271: Full-to-50 Sprint. Alle ausbaufaehigen Arrays auf >=50 Items skaliert (Astro/Geo/Sport/Tech/Tiere/Pflanzen/Gastro/Emob/Archaeologie/Kultur). 70x BETA-Praefixe entfernt. Jersey 15->50, Crest 10->50. verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
