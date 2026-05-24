@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 217 — H/L Proximity overhaul. getSmartMatch now uses log-ratio distance (scale-invariant) with 3x hard cap + top-6 cutoff so trivially obvious comparisons (London rain vs Cairo) are eliminated. genUniversalHLQ (Wolkenkratzer) now picks rank-adjacent buildings (+-4 positions) instead of fully random. Also: Phase 216 fake-country distractors, Phase 215 smart hyphenation, Phase 214 crash fixes."
git push origin main
pause
