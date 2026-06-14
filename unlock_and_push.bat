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
git commit -m "Content: Phase 575. medizin von 6 auf 8 Spiele aufgestockt: 2 neue Modi aus Bestandsfeldern - med_match_kategorie (Organ/Knochen/Meilenstein/Krankheit) + med_match_entdecker (Wer entdeckte das?). Damit haben ALLE Rubriken >=8 Spiele (ausser astronomie 7). Non-geo -> in NON_GEO_IDS.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
