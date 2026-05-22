@echo off
echo Removing stale git lock files...
if exist ".git\index.lock" del /f ".git\index.lock" && echo   deleted index.lock
if exist ".git\HEAD.lock" del /f ".git\HEAD.lock" && echo   deleted HEAD.lock
if exist ".git\refs\heads\main.lock" del /f ".git\refs\heads\main.lock" && echo   deleted main.lock
echo.
echo Committing...
git add -A
git commit -m "FIX: SLF-Timer 60s, Emoji-Unicode, Map-Zoom, X-Button sichtbar, Flashcard-Modulo, Lokal 1:1 Hot-Seat, Fussball-Modi"
echo.
echo Pushing...
git push origin main
echo.
echo Done! Press any key to close.
pause
