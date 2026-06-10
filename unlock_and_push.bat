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
git commit -m "Content: Phase 540. Neues Spiel 'Land -> Region' (geo_subregion, pure_geo): zeigt ein Land, waehle die Weltregion (Subregion) aus 4 Optionen. Nutzt COUNTRIES.sr + _SR_DE (lokalisiert), bestehender uk_match-Renderer. MODES + modes-Liste + GEN + genSubregionQ + i18n DE/EN/PL. Verifiziert: Samoa->Polynesien, Sudan->Nordafrika, alle loesbar; 1088->1089 Modi; Render 963 OK, smoke 957/0 THROW. Passt thematisch zum neuen Regionen-Feature.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
