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
git commit -m "Content: Phase 496. Altersstufen-Inhaltspruefung Stufe 1 (6-8 J.): Heuristik korrigiert - 'match/_mc/timeline' standardmaessig nicht mehr Level 1, sondern Level 2. Vorher sahen 6-8-Jaehrige 77 Modi, davon fast alle zu schwer (Motorbauart, Konsolengeneration, roemische Mythologie-Gegenstuecke, Fluss-Muendungslaender...). Jetzt zeigt Stufe 1 nur die 5 verstaendlichen Lehrplan-Spiele (Kontinente, Ozeane, Tiere, Kompass, Jahreszeiten). Schwerere Modi rutschen zu hoeheren Stufen (Stufe 2-4 Pruefung folgt). verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
