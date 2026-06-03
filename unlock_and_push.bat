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
git commit -m "Content: Phase 456. Lehrplan-konforme Alters-Tags: Grundschul-Sachunterricht (Kl. 1-4) behandelt Pflanzenwelt, Jahreszeiten/Wetter, Raum/Geografie/Karten, Sonne/Mond. Daher CAT_META audience um 'kids' erweitert fuer pflanzen, gartenbau, klima, fluesse, gipfel. Kinder-geeignete Modi 348->410/999 (per-Mode-Level-Filter blendet schwere Modi darin weiter aus). Spielübersicht zeigt automatisch 🧒-Marker + 'Kindgeeignet X/999'. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
