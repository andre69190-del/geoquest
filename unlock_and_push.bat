@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX+FEAT: Landscape-Exit, 8 HL-Generatoren (COMP_DATA), 17 HL-Beta-Modi, Fussball-Modi, Lokal-1:1, SLF-Timer-60s, Zoom-Fix, X-Button, Emoji-Fix, Flashcard-Modulo"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
