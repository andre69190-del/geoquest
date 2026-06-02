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
git commit -m "Content: Phase 424. 4 neue Geo/Zug-Modi: zug_match_land (177 Strecken→Land), odd_one_out (6 Kategorien: EU/NATO/Insel/Binnen/G7/Euro), clue_country (progressive Hinweise: Kontinent→Hauptstadt→Währung), sort_rank (4 Länder nach Metrik sortieren). MODES 810→814. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
