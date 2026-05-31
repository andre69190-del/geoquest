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
git commit -m "Content: Phase 328. ENGINE: Heimvorteil 70/30 in _mkMatchQ() — alle Match-Modi bevorzugen jetzt Einträge aus dem Heimatland des Nutzers (S.language → Ländername-Mapping, localPool, rng()<0.7). Fallback 100% global für nicht-geographische c-Felder.. verify: 138/138."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
