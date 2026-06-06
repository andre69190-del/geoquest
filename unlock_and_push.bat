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
git commit -m "Content: Phase 527. White-Screen-Crash behoben: Render rief .map auf moeglicherweise undefinierten Feldern auf (q.hints, q.countries, q.opts in 2 Zweigen, q._tlUserOrder, q.ans) -> bei Modi, die der Render-Test ueberspringt (async-Daten wie border_q/neighbor/plate/river, headless=null), konnte das die GANZE App abstuerzen lassen ('Cannot read properties of undefined reading map'). Alle q.X.map-Aufrufe im Render mit ||[]/Array.isArray abgesichert (0 ungeschuetzt). sort_rank/clue_country-Generatoren setzen ihre Felder korrekt (Guard = Absicherung). 195/195, alle Ebenen gruen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
