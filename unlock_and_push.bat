@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT+FIX: Phase 227-223-224 — Tiere & Natur + Pferde-DLC + Data Expansion + Greenlight Audit. Phase 227: 45 Tiere-Modi (15 Pin + 12 HL + 18 Match), Pferde-DLC (Rassen-Pin, Fachbegriffe-Match, Stockmass-HL, Pferdfluesterer-WS). QA-Hotfix: genUniversalPinQ strips location hints (Parens+Pfeil) from tiere-group subjects. Phase 223: Tiere/Pferde datasets scaled 20->29-68 entries (real data, no hallucinations). Search catLabels: tiere/natur/animals keywords added. Phase 224 Greenlight Audit: 0 KRITISCH/HOCH/MITTEL/LOW findings. Build: 1.581M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause