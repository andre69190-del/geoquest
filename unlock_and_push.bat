@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py || (echo. && echo [ABORT] verify.py FAILED - fix errors before pushing! && pause && exit /b 1)
echo.
git add -A
git commit -m "Fix+QA: Phase 243b+247. 243b: 32 fehlende MODES-Eintraege (Astro/Geo/Sport) -> Kategorien jetzt spielbar. 247: 16 HL-Ausreisser (z>4sigma) entfernt aus 6 Dateien (Sauerbraten 5760min, Balsamico 4380d, TPU-Pod, etc.) - La-Paz-Fenster greift jetzt korrekt. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
