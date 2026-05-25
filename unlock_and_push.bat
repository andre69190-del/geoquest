@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT/DATA: Phase 217/218 — Wort-Schmiede Overhaul. DE-Woerter: 5.3 → 31.0 Ø (max 80 pro Stadt). i18n Leer-Array-Fix (London-Falle). Neues UI: Buchstaben-Kacheln, Inventar-Check, Laengen-Scoring (3=10/4=20/5=40/6+=60pts), EN-Fallback-Badge. 111 Staedte."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause