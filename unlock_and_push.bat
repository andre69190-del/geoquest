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
git commit -m "Content: Phase 427. 2 neue Kategorien: Kino & Film + Musikgeschichte. 40 Filme + 40 Künstler (global: DE/FR/JP/PL/IN/KR/AU/CO). 15 neue Modi: 8x Film (H/L+Match+Timeline) + 7x Musik (H/L+Match+Timeline). Neue Generatoren genFilmeHLExt/MatchExt/genMusikHLExt/MatchExt. Validator-Update. MODES 814->829. verify: 148/148."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
