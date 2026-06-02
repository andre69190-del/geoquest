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
git commit -m "Content: Phase 413. Neue Kategorie 'Regionale Kultur & Kulinarik': 30 D-A-CH Einträge (Speisen, Weine, Getränke, Brauchtum), 6 Modi (Pin, 3x Match Land/Region/Kategorie, 2x H/L Alkohol/Saison), validate_content + i18n DE/EN/PL. MODES: 796→802. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
