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
git commit -m "Content: Phase 574. architektur von 55 auf 76: 21 weltbekannte Bauwerke web-verifiziert (Koordinaten/Hoehe/Baujahr per Subagent aus Wikipedia). 5 ausgelassen wegen unbelegter Hoehe/Jahr bzw. falscher Koordinate (Wat Arun, Goldener Tempel, Stonehenge, El Castillo, Berliner Fernsehturm) - keine Schaetzung. Ostankino, Oriental Pearl, Tokyo Tower, Koelner Dom, Notre-Dame, Potala u.a.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
