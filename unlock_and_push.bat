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
git commit -m "Content: Phase 342. Data Completion Sprint: Golf/Polo/Passat B1-B8, Corsa/Astra/Vectra, BMW 3er/5er, MB C/E-Klasse, Audi A3/A4, Peugeot/Renault, Fiat/Alfa, Škoda Octavia I-IV — 50 Jahre EU-Auto-Historie. verify: 139/139."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
