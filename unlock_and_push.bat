@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py || (echo. && echo [ABORT] verify.py FAILED - fix errors before pushing! && pause && exit /b 1)
echo.
git add -A
git commit -m "CONTENT: Phase 253+254. Geo+Sport Expansion — 70 neue Modi (12+8 Pin, 10+8 HL, 12+8 Match, 6+6 WS). MODES: 607->677. Geo: Felsformationen, Hoehlen, Canyons, Geysire, Fossilien, Ozeangraeben, Gletscher, Wuesten, Minen, Rifts, Nationalparks, Steilkuesten, Mohshaerte, VEI, Bohrtiefe, Tsunami u.v.m. Sport: Fussballstadien, Motorsport, Wintersport, Tennis, Skigebiete, Golf, Surfen, Klettern, Transferrekorde, Olympia-Gold, Stadionbaujahr u.v.m. ARCHITECTURE.md aktualisiert. verify: 89/89 | validate: 58 warnings."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
