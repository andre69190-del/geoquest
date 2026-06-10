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
git commit -m "Content: Phase 542. Region-Picker erweitert: (1) Lernkarten bieten Modus-Wahl - Hauptstaedte ODER Flaggen testen (startRegionQuiz mit capital/flag, beide respektieren den Sub-Filter). (2) Pro Kontinent-Gruppe ein Quiz-Button (startContinent -> _GRP_FILTER Europa->europe etc. -> ganzer Kontinent). i18n DE/EN/PL (Hauptstaedte/Flaggen). Verifiziert: Flaggen+Osteuropa regional, Kontinent-Filter, Buttons rendern.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
