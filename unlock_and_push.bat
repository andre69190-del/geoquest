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
git commit -m "Content: Phase 536. Politur: (1) Daily-Challenge-Karte vollstaendig i18n (DE/EN/PL) - 11 Stellen (Daily Challenge/erledigt/fortsetzen/Runde/Pkt./Endet in/Weiter/Spielen/Zug-Tag/Letzte 7 Tage/Neue Challenge in). (2) 3 restliche Icon-Buttons mit aria-label -> a11y 0 WARN. (3) Neuer informativer Check i18n_html_check.py: findet hartkodiertes Deutsch im HTML (Umlaut-Tag-Text + dt. title-Tooltips), das nicht ueber _tc laeuft - 30 Kandidaten (ueberwiegend Sekundaer-Screens), als Wegweiser.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
