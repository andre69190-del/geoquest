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
git commit -m "Content: Phase 421. UI-Feinschliff Spielkarten: mode-card kompakter (Padding .6rem .4rem 30px -> .5rem .32rem 28px, Radius 12px->11px), mode-icon 1.4rem->1.25rem, Info-Button (i) 32x32px->28x28px (Radius 7px, Font .72rem). Aenderungen in geoquest_css.txt (echte CSS-Quelle) + Info-Btn inline in gen.py. Leserlichkeit und Tap-Flaeche bleiben erhalten (Button >=24px WCAG). verify 146/146, validate 0 Warnings.. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
