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
git commit -m "Content: Phase 580. Fakten-Check-Korrekturen (unabhaengiger Subagent): Stephansdom baujahr 1578->1433 (136m=Suedturm 1433; 1578 war Nordturm-Haube); Qing-Dynastie Schluesselfigur Qianlong->Hong Taiji (Gruender 1636, konsistent zu start_jahr). Tyr->Norwegen belassen (Konvention aller nordischen Gottheiten).. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
