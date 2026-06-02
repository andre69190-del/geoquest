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
git commit -m "Content: Phase 425. Hilfe-Button sichtbar gemacht: ?-Button zusaetzlich in die sichtbare Home-Kopfzeile (_hdr, eingeloggt + Gast) neben das Feedback-Symbol gesetzt. Vorher nur in der GEOQUEST-Logo-Leiste, die auf dem Home-Tab nicht sichtbar ist -> Hilfe wurde nicht gefunden. verify 146/146, validate 0 Warnings.. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
