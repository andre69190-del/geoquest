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
git commit -m "Content: Phase 324. Gastronomie-Arrays geografisch ausbalanciert: nationalgerichte (+30), streetfood (neu, 32), hausmannskost (+20), suessspeisen (neu, 31) — Fokus Ziel-Länder EU-Ost/Nord/West. verify: 138/138."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
