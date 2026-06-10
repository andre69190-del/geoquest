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
git commit -m "Content: Phase 543. Neues Spiel 'Land -> Kontinent' (geo_continent, pure_geo): Land zeigen, Kontinent aus 4 waehlen. genContinentQ nutzt COUNTRIES.ct + _CONT_DE (lokalisiert). Kontinent-Namen + Prompt schon uebersetzt -> 0 neue i18n. 1089->1090 Modi. Verifiziert: Ungarn->Europa, Ghana->Afrika, Ecuador->Suedamerika. Gut fuer juengere Stufen.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
