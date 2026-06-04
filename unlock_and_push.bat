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
git commit -m "Content: Phase 505. 29 neue L1/L2 Modi: Astronomie(+4 L1), Capitals(+4 L1), Hunde(+4 L1), Map-Mode(+4 L1), Ozeane(+4 L1), Pure-Geo(+4 L1), Themeparks(+4 L1), Games(+1 L2: hl_digital_vk). Alle hardcoded emoji/flag-basiert, mitwachsend. i18n DE/EN/PL. 1059→1088 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
