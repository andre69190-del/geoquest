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
git commit -m "Content: Phase 532. Inhaltsfeinschliff emob_match: bidirektional (c hatte Muell wie Deutschland/Wirtschaftlichkeit/Batterieverschleiss + Varianten V2H Backup/V2G Japan) auf saubere V2H/V2G/V2L/V2V normalisiert (n-basiert zugeordnet); level_autonomy Varianten (Level 4/5/2+/0/4 begrenzt) auf die 4 Stufen gemappt. Beide jetzt 100% in fixedOpts -> klare 4-Optionen-Fragen. Andere emob-Kategorien (stecker/zellchemie/motorentypen/...) BEWUSST belassen: ihre reicheren c-Werte (J1772/NACS/...) sind korrekter als ein Zwang in 4 Buckets und liefern nach Phase 515 bereits praezise Fragen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
