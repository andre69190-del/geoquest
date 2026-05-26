@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 227 Part 1 — Tiere & Natur Kategorie (21 Modi): 10 Pin-Modi (Endemische Arten, Big Five, Grosskatzen, Invasive Arten, Vogelzug, Haustiere-Ursprung, Nationaltiere, Primaten, Hai-Hotspots, Baeren) + 11 H/L-Modi (Gewicht Land/Meer, Speed Land/Luft/Wasser, Lebenserwartung, Traechtigkeit, Wurfgroesse, Giftigkeit, Population, Schlaf). genTiereHL mit La-Paz-Windowing + parseFloat. 200 Geo-Datenpunkte. Build: 1.481M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause