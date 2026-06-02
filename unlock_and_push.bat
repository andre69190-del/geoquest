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
git commit -m "Content: Phase 428. 2 neue Kategorien: Mythologie & Sagenwelt (40 Gottheiten: GR/NO/AE/RO/JP/AZ/MES) + Architektur & Megabauten (40 Bauwerke: Wolkenkratzer/Brücken/Staudämme/Tunnel/Tempel/Denkmäler). 11 neue Modi: myth_match_domain/kultur/typ/roemisch + myth_pin_herkunft + hl_arch_height/span/baujahr + arch_match_land/typ + arch_pin_megaprojects. MODES 829->840. verify: 150/150."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
