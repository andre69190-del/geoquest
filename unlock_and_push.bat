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
git commit -m "Content: Phase 539. Lern-/Uebungsmodus (Lernkarten vor dem Test), integriert in den Region-Flow: Region-Chip oeffnet jetzt eine Lernkarten-Strecke (renderLearnDeck) mit Flagge + Land + Hauptstadt + Vor/Zurueck + 'Jetzt testen' -> startRegionQuiz('sub:X','capital'). _capByCc nutzt CAPITALS. So 'erst lernen, dann testen' (haeufiger Seterra-Wunsch) + Sub-Regionen kombiniert. i18n DE/EN/PL. renderRegionEntry/Modal/LearnDeck im Render-Test abgedeckt. Alle Ebenen gruen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
