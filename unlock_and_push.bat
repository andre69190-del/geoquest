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
git commit -m "Content: Phase 488. Lernspiel 3/5: Die 5 Ozeane (ozean_finder, Kategorie ozeane). genOzeanFinderQ: Frage (groesster/tiefster/umgibt Antarktis/Nordpol/bei Indien/zwischen Amerika+Europa) -> Ozean-Name antippen (uk_match). Mitwachsend: Stufe 1 nur 3 einfache Fragen, ab Stufe 2 alle 7. 5 Ozeane Pazifik/Atlantik/Indik/Arktik/Suedpolarmeer. i18n mt_ozean/ocn_*/ocq_* de/en/pl. Lehrplan KS1 '5 Ozeane'. verify 193/193, 0 THROW, 1002 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
