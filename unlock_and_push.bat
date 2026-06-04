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
git commit -m "Content: Phase 482. i18n Hot-Seat-Screen: alle hartkodierten DE-Strings (Titel, Untertitel, SPIELMODUS/RUBRIK/SPIEL WÄHLEN, Zufall/Rubrik/Spiel, Spiel starten, Handoff-Hinweis, Ich bin bereit, gewinnt/Unentschieden, Nochmal spielen, Hauptmenü) -> t() in de/en/pl (lv_*). Zurück-Button von links nach rechts (align-self:flex-end). verify 193/193.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
