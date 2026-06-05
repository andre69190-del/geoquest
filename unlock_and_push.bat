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
git commit -m "Content: Phase 513. Test-Suite gehaertet+dokumentiert: ingame_render_test.js (In-Game-Render-Test aller 1088 Modi, 943 OK 0 Render-Fehler) verfeinert - Timeline-Feedback uebersprungen (braucht Drag-Zustand), ans-in-opts nur fuer uk_match mit Klammer-Bereinigung als Info (31 Treffer zur spaeteren Pruefung). Session-Starter um TEST-SUITE-Sektion ergaenzt: verify.py + validate_content.py + node smoke_test.js + node ingame_render_test.js, jeweils mit Sollwerten und Bug-Klassen-Erklaerung.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
