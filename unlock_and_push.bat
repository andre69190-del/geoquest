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
git commit -m "Content: Phase 467. UX-Review Paket 4+6 + Greeting-Fix: (4) Zuletzt-gespielt als breite Wisch-Karten (152px, Icon links + 2-Zeilen-Text rechts, laeuft rechts raus = Wisch-Signal). (6) Pastell-Themen pro Kategorie: _catTint(k) leitet aus CAT_META-Interesse eine dezente rgba-Toenung ab (geo blau, natur gruen, mint lila, pop pink, kultur amber, sport orange) - funktioniert hell+dunkel, gegen Box-in-Box. (Fix) Begruessung wieder einzeilig (nowrap), Globe aus Gast-Gruss entfernt (war in 2. Zeile gerutscht). verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
