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
git commit -m "Content: Phase 465. Home-Strips poliert: (1) Zuletzt-gespielt zeigt unterscheidbaren Titelteil nach ': ' (statt 4x 'Regionale Kultur: ...'). (2) 'Fuer dich' via _forYouCats() auf ~6 Vorschlaege aufgefuellt (topCats + Interessen + populaere Fallbacks, kindgefiltert, dedupliziert). (3) Begruessung darf umbrechen statt abzuschneiden (kein nowrap/ellipsis mehr). verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
