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
git commit -m "Content: Phase 470. Zuletzt-gespielt-Leiste vereinheitlicht: (1) Pastell-Toenung pro Karte via _catTint - neue Helper _recCat(mid) findet die Kategorie des Modus in MODE_CATS, gleicher Look wie Kategorie-/Empfehlungskarten. (2) Anschnitt sauberer: rechter Verlauf von 32px auf 52px verbreitert + ab 70% deckend (kein harter Wort-Abriss mehr), scroll-snap-type:x proximity + scroll-snap-align:start fuer sauberes Wischen. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
