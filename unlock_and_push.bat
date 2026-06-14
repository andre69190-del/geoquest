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
git commit -m "Content: Phase 578. tiere_kontinent von 12 auf 17: 5 eindeutig einem Kontinent zuzuordnende Tiere ergaenzt (Nilpferd/Gorilla->Afrika, Pfau/Orang-Utan->Asien, Truthahn->Nordamerika). Nur Single-Kontinent-Tiere (keine mehrdeutigen wie Nashorn/Leopard). essen_land vorher 9->16.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
