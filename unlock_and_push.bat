@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 204 — 15 neue Airport+Spezial-Modi: Flugrouten-Duell, Inlandsflug, Sunrise-Guesser, Aequator-Magnet, Kontinent-Klicker, Hauptstadt-Distanz, IATA-Reverse, Jetlag, Klima-Daten, Insel-Festland, Sprachen-Kompass + gqDist Haversine"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
