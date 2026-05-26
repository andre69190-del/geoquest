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
git commit -m "FIX+FEAT: Phase 228-231 + Bugfixes + Polish + Refactoring. Tiere/Pflanzen Split. Phase 229 Gastronomie. Phase 230 Tech+E-Mob. Phase 231 Archaeologie. BUGFIX: genUniversalPinQ {prompt,items}-Format. Polish WS: 4680 Woerter. Refactoring: 16 Generatoren -> 4 Factories. _CAT_ORDER dynamisch. verify.py Null-Bytes. MODES: 692. verify: 53/53."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
