@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT+FIX: Phase 227 Parts 1-4 + Pferde-DLC + QA-Hotfix — Tiere & Natur Kategorie (45 Modi): 15 Pin-Modi + 12 H/L-Modi + 18 Match-Modi. Pferde-DLC: Pferderassen-Pin, Fachbegriffe-Match, Stockmass-HL, Pferdfluesterer-WS. QA-Hotfix: genUniversalPinQ strips location hints (Parens+Pfeil) from tiere-group subjects to eliminate map spoilers. Build: 1.535M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause