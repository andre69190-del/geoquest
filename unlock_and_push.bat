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
git commit -m "Content: Phase 507. Spielübersicht: neue Spalte 'Altersstufen' zeigt farbige Badges (1=6-8J grün, 2=8-10J blau, 3=11-13J lila, 4=14-15J orange) pro Modus. _mode_level vollständig mit gen.py synchronisiert (L1-Hardcode-Liste, TEEN/HID-Tokens, HARD-Keywords Level 5). _grade_badges() berechnet Sichtbarkeit je Alterskategorie. generate_spieluebersicht.py aktualisiert.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
