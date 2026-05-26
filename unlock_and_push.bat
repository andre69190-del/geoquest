@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 227 Parts 1+2 — Tiere & Natur Kategorie (33 Modi): 10 Pin-Modi + 11 H/L-Modi + 12 Match-Modi (Faehrten, Architekten, Tarnung, Ernaehrungstypen, Symbiosen, Tauchtiefe, Mimikry, Metamorphose, Biolumineszenz, Anatomie, Tierlaute, Sinnesleistungen). genTiereHL (La-Paz-Windowing+parseFloat) + genTiereMatchQ (Cross-Cat-Distractors+fixedOpts). 200 Geo-Datenpunkte + 240 Match-Eintraege. Build: 1.505M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause