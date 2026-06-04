@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py
if errorlevel 1 (
    echo.
    echo ABORT: verify.py FAILED - fix errors before pushing!
    pause
    exit /b 1
)
echo.
git add -A
git commit -m "Content: Phase 480. Spiel-Empfehlungen: _forYouGames() schlaegt einzelne Spiele vor (ab 5 Spielen, Mix 60% neu / 40% bewaehrt aus Top-Kategorien + Interessen, Kinder-Filter, nur spielbare GEN). Neue Home-Leiste '🎯 Empfohlene Spiele' (_renderGameStrip) mit Pastell-Tint + Mausrad/Touch-Scroll. Abschaltbar via Einstellungs-Schalter gq_rec_games (Standard an). i18n rec_games_title/rec_setting/rec_sub in de/en/pl.. verify: 192/192."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
