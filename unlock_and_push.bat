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
git commit -m "Content: Phase 485. Altersstufen erweitert: _kidLevelMax jetzt 1-4 (gq_kids_grade 1/2/3/4). _modeLevel: Erwachsenen-Trivia (HARD-Keywords + Jahr/Metacritic-Signale) jetzt Level 5 statt 3 -> bleibt selbst fuer Stufe 4 (14-15) ausgeblendet, nur 16+ sieht es. Grade-Selektor in Einstellungen auf 4 Stufen erweitert (6-8/8-10/11-13/14-15) + flex-wrap, i18n kids_grade_t3/t4 de/en/pl. verify 193/193, Rauchtest 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
