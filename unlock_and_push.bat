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
git commit -m "BUGFIX: Phase 235-237. [BETA] tags stripped (318). WS validWords uppercase+anagrams fixed (2746/724). q.ans null guard. archaeologie_match 31 dupes. validate_content.py hardened. _mkMatchQ no-padding. emob port_position n/c swap. HL dupes renamed. verify: 53/53."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
