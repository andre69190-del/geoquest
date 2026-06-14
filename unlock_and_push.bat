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
git commit -m "Content: Phase 579. 4b-Kinderspiele aufgestockt (akkurate Inline-Items): tiere_haustier_wild 12->18, tiere_wasser_land 12->17, tiere_gross_klein 12->17, pflanze_farbe 8->14 (neue Farben blau/orange), pflanze_essbar 8->12. Nur eindeutige Tiere/Pflanzen.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
