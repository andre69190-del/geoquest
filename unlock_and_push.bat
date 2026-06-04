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
git commit -m "Content: Phase 468. Greeting-Fix i18n: 🌍 auch aus PL/FR/ES/IT/BG home_guest entfernt (war nur DE/EN entfernt) - sonst gleiches Umbruch-Problem in 5 Sprachen. Polnisch 'GoŚ›ciu'-Korruption -> 'Gościu' repariert. Alle 7 Gast-Gruesse jetzt einzeilig & globe-frei. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
