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
git commit -m "SECURITY+QA: Phase 249. submitRouteResult() extrahiert -> _TRUSTED_FNS (Anti-Cheat). PWA-Banner DOM-Fix (beforeinstallprompt->render()). LocalStorage TTL 90d (Date.parse statt timestamp). run_patch.py: validate_content.py nach verify.py. verify: 89/89 | validate: 49 warnings."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
