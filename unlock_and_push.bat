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
git commit -m "Content: Phase 529. Testluecke async-Modi geschlossen: ingame_render_test seedet jetzt NEIGHBORS=_DEFAULT_NEIGHBORS (Live-Fallback, da neighbors.json leer ist) und transformiert rivers/license_plates/area.json direkt ins Zielformat (Parser sind inner-scoped, nicht aufrufbar). Dadurch werden border_q/neighbor/river_real/plate/hl_area jetzt wirklich gerendert (955->962 OK, 0 Render-Fehler). Diese Modi waren bisher ungetestet (headless=null) und der Weg, ueber den der White-Screen-Crash durchrutschte.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
