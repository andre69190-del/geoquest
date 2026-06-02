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
git commit -m "Content: Phase 429. 2 neue Kategorien: Literatur & Comics (40 Werke: Roman/Comic/Manga/Kinderbuch global) + KI, Robotik & Hardware (40 Systeme: WRO/FLL/Arduino/ChatGPT/AlphaGo/KUKA). Fix: MYTH_DATA/ARCH_DATA Placeholder-Bug (Phase 428 retrofix). 12 neue Modi: hl_lit_sales/release + lit_match_autor/land/protagonist + timeline_lit_release + hl_robot_jahr + robot_match_kategorie/land/entwickler/fakt + timeline_robot_jahr. MODES 840->852. verify: 152/152. verify: 152/152."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
