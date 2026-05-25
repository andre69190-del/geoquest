@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT+SEC: Phase 216 — 52 new [BETA] modes + Deep System Audit. Schritt 1-4 komplett: 9 Universal-Pin, 9 H-L-Beta, 26 Universal-Match, 8 Spezial-Modi. genFixedPoolMatchQ Engine neu. HL_BETA_DATA auf 44 Laender, 9 neue Metriken. getSmartMatch log(0)-Guard. Accordion Single-Open UX. See commit fa55f74 fuer Details."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause