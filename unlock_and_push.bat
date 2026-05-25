@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 222 — Stadium-Hoehe dynamisch (22 Stadien, Index-Rank-Proximity, kein La Paz vs Muenchen mehr), getSmartMatch 10%-Fenster (statt fix 2-5), Binary-Pool-Bug (4x Nein) behoben, D3-Karte kein Weiss-Screen mehr (translateExtent), Kategorie-Reset-Bug (filterCat), HL_BETA 45 Laender-Flags. Build: 1.450M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause