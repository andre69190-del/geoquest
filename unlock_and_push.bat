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
git commit -m "DATA+QA: Phase 248. WS-EN-Fallback: validWords.en fuer 9 Modi (astro/geo/sport_ws). pflanzen_match: bestuaeber-Korruption gefixt + Mais-Duplikat entfernt. pflanzen_pin: nationalblumen wiederhergestellt (20 Items) + Klee-Duplikat entfernt. validate: 37/37 OK | 49 warnings. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pau