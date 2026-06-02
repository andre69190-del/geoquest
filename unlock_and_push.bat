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
git commit -m "Content: Phase 431. Phase 431: Kategorien Anatomie & Medizin + Wirtschaft & Marken. 13 neue Modi (6 Medizin, 7 Wirtschaft). Neue Dateien: medizin_extended.json (40), wirtschaft_extended.json (40), medizin_ws.json, wirtschaft_ws.json. MODES: 861→874. verify: 159/159."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
