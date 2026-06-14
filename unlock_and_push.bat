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
git commit -m "Content: Phase 566. Neues Geo-Feld (echte Daten): architektur.json um 'stadt' fuer alle 40 Bauwerke erweitert (akkurat, weltbekannt) + neues Spiel arch_match_stadt 'In welcher Stadt steht dieses Bauwerk?'. Beweis: neue Felder ermoeglichen neue interessante Geo-Spiele (nicht nur ableiten). 1096->1097.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
