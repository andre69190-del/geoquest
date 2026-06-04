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
git commit -m "Content: Phase 494. Onboarding-Alter (auf Nutzerwunsch) + 2 Fixes: (1) Bei Auswahl Kind/Jugendlich erscheint darunter eine Altersstufen-Auswahl (Kind: 6-8/8-10, Jugendlich: 11-13/14-15) -> setzt gq_kids_grade praezise; nur bei Kind/Jugendlich sichtbar, keine Reibung fuer Erwachsene. finishOb nutzt S.obGrade (validiert je Audience). (2) btn_next: ueberfluessiges Hochkomma nach Pfeil in ALLEN Sprachen entfernt (Weiter →' -> Weiter →). (3) Landing: .nav-cta Kontrast gefixt (.nav-links a ueberschrieb color:#fff -> Spezifitaet erhoeht, weisser Text auf gruen). verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
