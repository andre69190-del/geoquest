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
git commit -m "REFACTOR+DOCS: Phase 225-226 — JSON Separation + Patches System + Selftest + Architecture Handbook. Phase 225: Extracted KULTUR_DATA+TIER_WS/HL/MATCH_DATA to data/*.json (118 KB out of gen.py, 1.19MB->1.07MB). Suggestion 1: patches/ dir + PATCHES.md convention + run_patch.py (auto-backup, build, verify, rollback). Suggestion 3: verify.py (33 checks: JS syntax, data objects, MODES count, generators, anti-cheat, mojibake, _GQ_SALT) as pre-push gate in bat. Phase 226: ARCHITECTURE.md -- full system doc: build pipeline, 4 universal engines (Pin/HL/Match/WS), Zero-Bug-Workflow, S-object, Anti-Tamper, Anti-Cheat proxy, localStorage schema. Build: 1.640M chars."
echo.
echo Pushing to GitHub...
git push origin main
echo.
echo Done! Check Vercel for deployment.
pause