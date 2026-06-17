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
git commit -m "Content: Phase 581. Mastery sichtbar (#2, forschungsbasiert): 'Gemeistert'-Zaehler (gq_srs_mastered) wird erhoeht, wenn eine Frage Leitner-Box 5 erreicht; Anzeige im Schwaechen-ueben-Hero ('n faellig . X gemeistert'). #3 (Farbenblind-Feedback) war bereits erfuellt: Antworten zeigen schon Symbole ✓/✗ zusaetzlich zur Farbe.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
