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
git commit -m "DATA: Phase 245 Hotfix. geo_ws: ITALIA+BEENDEN entfernt. sport_ws: TORION+FLUSS entfernt. tiere_pin: {prompt,items} Struktur. astro/geo/sport_pin Struktur-Fix. WS-Duplikate bereinigt (stalaktiten TALENT, sternwarte). verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
