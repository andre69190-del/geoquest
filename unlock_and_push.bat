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
git commit -m "Content: Phase 577. essen_land von 9 auf 16 Gerichte erweitert (eindeutige Herkunft, Windows-sichere Emojis): +Pasta(IT), Fondue(CH), Waffel(BE), Burrito(MX), Donut(US), Mooncake(CN), Onigiri(JP). Neue Laender Schweiz/Belgien.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
