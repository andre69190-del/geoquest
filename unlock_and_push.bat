@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT/FIX: Phase 219+220 — Grand Finale Sprint. Audit-Fixes: HTML-Syntax (3 Modi), 6 neue Pin-Modi (Bruecken/Filmsets/Kirchen/Kunstwerke/Ruinen/Weinregionen) je 15 Eintraege mit GPS, museen lat/lng ergaenzt (30 Museen), Mojibake ES/FR/CS/BG geheilt. Streak-System: taegliche Serie mit Feuer-Badge im Homescreen. 52x [BETA]-Tags entfernt (Produktion-ready). Viewport user-scalable=no. Build: 1.44M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause