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
git commit -m "Content: Phase 523. uk_pin/airport_pin Feedback-Bug: bei Timeout (Frage ueber generisches answer(null) beantwortet, S.sel='__t') blieb airportPinDist ungesetzt -> Anzeige '✗ 0 km entfernt' (widerspruechlich: 0 km waere perfekt). Fix: Pin-Feedback prueft S.sel==='coord' (echter Pin); sonst Meldung 'Zeit abgelaufen – kein Pin gesetzt' (DE/EN/PL in i18n_extra). build_i18n_extra.py um EXTRA_UI erweitert + Writer schreibt Zusatz-Strings. 195/195, i18n 0 Luecken.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
