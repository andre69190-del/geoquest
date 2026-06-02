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
git commit -m "Content: Phase 423. Hilfe-Funktion: dauerhaftes Hilfe-Overlay per neuem ?-Button im Header (renderHelpModal). Erklaert kindgerecht die Spiel-Typen (H/L, Match, Pin, Wort-Schmiede, Multiple-Choice), Schwierigkeit (Casual/Hardcore/Survival), Coins, Favoriten, Suche, Kategorie-Leiste. i18n DE/EN/PL (19 Keys je Sprache). verify 146/146, validate 0 Warnings.. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
