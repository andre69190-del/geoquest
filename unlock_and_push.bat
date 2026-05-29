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
git commit -m "Phase 288: Polnische Spielinhalte 5 Rubriken (patch_288_pl_content_i18n.py): erweiterbares _CONTENT_I18N + _tc(); 196 Prompts + 54 Einheiten + 79 Match-Buttons auf Polnisch, in Universal-Engines verdrahtet. 685 Modi. verify: 90/90."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
