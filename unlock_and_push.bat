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
git commit -m "BUGFIX: Phase 235+236. Fix 1: Strip 318 [BETA] tags. Fix 2+3: WS validWords uppercase + invalid anagrams removed (2746/724). Fix 4: q.ans null guard. Fix 5: archaeologie_match 31 dupes. Fix 6: validate_content.py kultur dispatch + round-coord. verify: 53/53."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
