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
git commit -m "Content: Phase 568. geschichte_extended von 40 auf 66 erweitert: 26 grosse Reiche web-verifiziert (Spitzenflaeche aus Wikipedia 'List of largest empires'; Datum/Hauptstadt/Schluesselfigur stabile Fakten) - Qing, Spanisches/Franzoesisches Kolonialreich, Umayyaden, Yuan, Tang, Maurya, Sassaniden, Timuriden, Safawiden, Song, Sui u.a. Bereichert hist_match_zentrum/hl_hist_*.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
