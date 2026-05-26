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
git commit -m "REFACTOR: Phase 225 + Suggestions 1+2+3 — Data-Logic Separation + Patches System + Build Selftest. Phase 225: Extracted KULTUR_DATA+TIER_WS/HL/MATCH_DATA to data/*.json (118 KB out of gen.py). gen.py: 1.19MB -> 1.07MB. Suggestion 1: patches/ directory with PATCHES.md convention + run_patch.py runner (validate+patch+build+verify, auto-rollback on failure). Suggestion 2: JSON separation complete (Node.js round-trip validated). Suggestion 3: verify.py selftest (33 checks: JS syntax, data objects, MODES count, generators, anti-cheat, mojibake, JSON validity, _GQ_SALT). verify.py now hooked into unlock_and_push.bat as pre-push gate. Build: 1.640M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause