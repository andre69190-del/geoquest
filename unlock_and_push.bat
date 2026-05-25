@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "DATA: Phase 217 — Wort-Schmiede Datenanreicherung. DE-Woerter: Ø 5.3 → 10.8 pro Stadt (111 Staedte). Wordfreq-basierte Anreicherung + 300 kuratierte Kernwoerter. Min 1 / Max 15. Spiele wie FRANKFURT(15), ISTANBUL(15), AMSTERDAM(15) voll ausgebaut."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause