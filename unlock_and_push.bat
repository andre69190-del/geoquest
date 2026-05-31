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
git commit -m "Content: Phase 326. Natur-Balancing: nationaltiere (+27), nationalpflanzen (+28), gewuerze (+17), nationalblumen (+15) — 16 Ziel-Länder EU-Ost/Nord/West abgedeckt. verify: 138/138."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
