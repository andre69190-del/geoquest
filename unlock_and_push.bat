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
git commit -m "Content: Phase 343. Data Completion Sprint 330c: BMW 1er/7er/X5, MB S/A/SL/G-Klasse, Audi A8/TT, Porsche Boxster/Cayenne, Opel Manta/Calibra, Ford Fiesta/Focus/Capri/Sierra, Volvo 240/V70/XC90, Saab, Smart W453, Mini. verify: 139/139."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
