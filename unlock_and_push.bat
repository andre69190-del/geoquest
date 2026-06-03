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
git commit -m "Content: Phase 455. Spiel-Ebene-Filter fuer Kinder-Modus: _modeLevel(m) bewertet Modi heuristisch (1 leicht / 2 mittel / 3 schwer) nach Mechanik (Match=1, H/L=2, Wort-Schmiede=3) + harten Schluesselwoertern (Metacritic, PEGI, Hubraum, BGG, Oscars u.a.). _kidHidden(m) blendet im Kinder-Modus Level-3-Modi auch innerhalb erlaubter Kategorien aus (catModes-Filter). Loest: zu schwere Spiele wie Auto-Hubraum/Game-Metacritic in Kinder-Kategorien. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
