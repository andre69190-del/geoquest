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
git commit -m "Content: Phase 414. Dual Menu Layout: Tab-Ansicht (3 Reihen × 8 Kategorien) + Settings-Toggle gq_menu_layout (accordion/tabs). CSS-Klasse tabs-mode blendet Akkordeon-Header aus, Carousel-Logik unverändert. verify: 146/146. verify: 146/146."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
