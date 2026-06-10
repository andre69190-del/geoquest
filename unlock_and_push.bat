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
git commit -m "Content: Phase 534. Spaced Repetition / Fehler-Training (Leitner): Falsch beantwortete Fragen werden als Snapshot in gq_srs erfasst (answer + answerAirportPin, nur replaybare Typen MC/HL/Pin). Boxen 1-5 mit Intervallen (0/0/2/5/12 Tage), Box 5 = gemeistert (entfernt). Neuer Modus 'Schwächen üben' (startSrsReview/srsNext) spielt faellige Items wieder; nextRound erkennt S.srsRun und ruft srsNext. Home-Card renderSrsHero zeigt Faelligkeits-Zahl (nur wenn >0). i18n DE/EN/PL. Verifiziert: Erfassen/Box-Logik/Mastery/Review-Start korrekt. Adressiert den haeufigsten App-Store-Wunsch (smart review statt Zufall).. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
