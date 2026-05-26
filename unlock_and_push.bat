@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT: Phase 227 Parts 1-4 + Pferde-DLC — Tiere & Natur Kategorie (45 Modi): 15 Pin-Modi + 12 H/L-Modi + 18 Match-Modi (inkl. Darwin-Finken, Schutzgebiete, Zoos, Nutztierrassen, Fossilien, Arktis/Antarktis, Forscher-Eponyme, Pelagial, Wuesten, Gift-Hotspots, Migranten, Haustier-Dichte). Pferde-DLC: Pferderassen-Pin, Fachbegriffe-Match, Stockmass-HL, Pferdfluesterer-WS. Build: 1.535M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause