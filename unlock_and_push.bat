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
git commit -m "Content: Phase 520. Kosmetik lange Optionen: .opt-btn line-height:1.25 (kompaktere mehrzeilige Buttons) + Media-Query max-width:360px (kleinere Schrift fuer .opt-btn/.btn-a). KEIN Datenkuerzen — Texte brachen schon sicher um (word-break/overflow-wrap/hyphens vorhanden, kein Clipping). 37 Modi mit Option>42 Zeichen betroffen, jetzt sauberer auf schmalen Screens.. verify: 194/194."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
