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
git commit -m "Content: Phase 497. Altersstufen-Inhaltspruefung Stufe 2 (8-10 J.): nicht-curriculare Trivia-Kategorien (Games, Autos, Mythologie, Literatur, Brettspiele, Zuege/Bahn-Technik, Konsolen) + Zeitleisten auf Level 3 (Teens) gehoben - via Token-Treffer im Modus-Namen (auto/games/konsole/hw_/myth/lit_/boardgame/zug/bahn/timeline), faengt auch hl_-Varianten. Stufe 2 zeigt jetzt Geografie+Natur (Flaggen, Hauptstaedte, Fluesse, Kontinente, Tiere, Pflanzen, Themenparks, Hunde, Astro/Geo-Vergleiche). verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
