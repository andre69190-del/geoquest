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
git commit -m "Content: Phase 546. Handbuch aktualisiert: neuer Abschnitt 'Lernen & Wiederholen' (guide_p7) im Eltern-Tab dokumentiert Daily Challenge (+ teilen, Streak-Kalender), Schwächen üben / Spaced Repetition / Fehler-Tagebuch (+ an/aus) und Region üben / Lernkarten. DE/EN/PL. Bisher war keines der neuen Features dokumentiert. Verifiziert in allen 3 Sprachen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
