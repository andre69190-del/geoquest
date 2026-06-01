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
git commit -m "Content: Phase 352. ENGINE SPRINT 352: Auto-Universum komplett — 25 neue Modi (12 H/L + 8 Match + 5 kreativ). AUTOS_EXT_DATA (431 Fzg., 22 Felder) inline. genAutosHLExt + genAutosMatchExt + Baujahr-MC + Leistungsgewicht + CO2 + Dekaden-Quiz.. verify: 140/140."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
