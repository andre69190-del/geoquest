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
git commit -m "Content: Phase 474. Kategorie-Strips (_renderPlaylistStrip: Empfohlen + Gruppen) liefen rechts hart abgeschnitten raus. Jetzt wie die Zuletzt-gespielt-Leiste: weicher rechter Verlauf (46px, ab 72% deckend), padding-right 40px fuer Anschnitt-Hinweis, scroll-snap fuers Wischen. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
