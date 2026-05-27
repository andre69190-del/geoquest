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
git commit -m "Fix+QA: Phase 243b+247. 243b: 32 fehlende MODES-Eintraege (Astro/Geo/Sport) -> Kategorien spielbar. 247: HL-Extremwerte wiederhergestellt, validate_content.py z>4sigma als [INFO] statt Warnung (La-Paz-Fenster schuetzt Gameplay). ARCHITECTURE.md §3.2 Outlier-Regel ergaenzt. verify: 89/89 | validate: 51 warnings."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
