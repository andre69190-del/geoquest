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
git commit -m "Content: Phase 570. mythologie von 40 auf 88 erweitert: 48 bekannte Gottheiten/Wesen (Griechisch/Nordisch/Aegyptisch/Roemisch/Japanisch/Aztekisch/Mesopotamisch + neue Kultur Keltisch). Stabile, belegte Fakten; Koordinaten = Kultur-Region wie Bestandsdaten. Bereichert myth_match_domain/kultur/typ/land + myth_pin_herkunft.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
