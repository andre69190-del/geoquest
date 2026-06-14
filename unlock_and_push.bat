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
git commit -m "Content: Phase 563. Rubrik-Merge (nicht-destruktiv): duenne Trivia-Rubriken zusammengelegt. Absorbiert: hunde->tiere, gartenbau->pflanzen, regional->gastronomie, hl_compare->comparisons, robotik/autos/wirtschaft->technologie (jetzt 'Technik & Industrie'). Neue Sammel-Rubriken: 'Pop & Medien' (filme/serien/musik/webkultur/boardgames), 'Kunst, Kultur & Geschichte' (kunst/literatur/architektur/mythologie/geschichte/sprachen). 29 Geo-Rubriken, alle >=8 ausser astronomie/inseln/gipfel(7). 0 verwaiste Modi. Per MODE_CATS-Postprocessing + _MERGED_CHILDREN-Filter, keine Modi geloescht.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
