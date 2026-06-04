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
git commit -m "Content: Phase 508. UX: Leere Kategorien im Kinder-Modus pro Stufe ausblenden. Neuer Helfer _catKidCount(k) zaehlt sichtbare (nicht _kidHidden) Modi einer Kategorie; _CAT_ORDER-Kinderfilter blendet Kategorien mit 0 Modi fuer die aktuelle Stufe aus. Ergebnis: Stufe 1 zeigt 14 statt 24 Kategorien (keine leeren wie Inseln/Gipfel/Autos/Games), Stufe 2 zeigt 22, Stufe 3/4 alle 24. Kein Kind tippt mehr auf eine leere Kategorie. verify 193/193, 0 THROW, 1088 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
