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
git commit -m "Content: Phase 477. Kategorie-/Recent-Reihen am Desktop scrollbar gemacht: ohne sichtbare Scrollbar + ohne Touch kam man an die angeschnittenen Kacheln nicht ran ('wischen geht nicht'). Neuer onwheel-Handler wandelt vertikales Mausrad in horizontales Scrollen (this.scrollLeft+=deltaY), preventDefault nur solange die Leiste noch scrollen kann -> Seiten-Scroll am Ende frei. cursor:grab als Hinweis. Touch-Wischen unveraendert nativ.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
