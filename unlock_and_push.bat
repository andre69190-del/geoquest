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
git commit -m "FIX+FEAT: Phase 228-232. Tiere/Pflanzen Split. Gastronomie+Tech+E-Mob+Archaeologie. BUGFIX: targetLat/targetLng in _mkPinQ. BUGFIX: Feedback-Pill zeigt echte Punkte. BUGFIX: Kartenlabel-Overflow. BUGFIX: genUniversalPinQ Dual-Format. _CAT_ORDER dynamisch. Polish WS 4680 Woerter. MODES: 692. verify: 53/53."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
