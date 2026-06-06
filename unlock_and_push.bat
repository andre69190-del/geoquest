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
git commit -m "Content: Phase 526. Rest-i18n: spielerseitige UI-Labels gewrappt (_tc): Verfuegbare Buchstaben:, Ueberpruefen, Schliessen, WOERTER, Keine Woerter gefunden, Laender/Staedte (Logik-Gitter), Zum Menue. Uebersetzungen EN/PL in i18n_extra.json + build_i18n_extra.py EXTRA_UI (reproduzierbar). i18n 0 Luecken, alle 8 Test-Ebenen gruen. Bewusst NICHT uebersetzt (edge): Admin-Panel, Ad-Platzhalter, Absturz-Screen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
