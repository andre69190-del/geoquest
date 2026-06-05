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
git commit -m "Content: Phase 511. GROSSER ABSTURZ-FIX (74 Spiele): die parallel ergaenzten einfachen Kinder-Modi gaben type:uk_match mit FALSCHEN Feldnamen zurueck (question/options/correct statt subj/opts/ans) -> Renderer q.subj.replace(undefined) -> App-Absturz beim Spielen. Zentrale Schema-Normalisierung in lq() eingefuegt (question->subj, options->opts, correct->ans, fehlender prompt aus Modus-Titel, fehlende lid generiert, timeline-items label->n). Zusaetzlich Optionen-Render gehaertet (String(o).replace statt o.replace -> numerische Optionen wie FCI-Gruppe 9). In-Game-Render-Test (alle 1088 Modi im Spiel-Screen): 942 OK, 0 echte Fehler. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
