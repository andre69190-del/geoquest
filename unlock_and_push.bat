@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "RELEASE: Phase 218 — Beta-Labels entfernt. Alle 9 Stellen mit Emoji+[BETA]-Prompt-Prefix (genHLBeta, HL_BETA_METRICS, genBetaMCQ/HL/Spotter) bereinigt. Spiele sind produktionsreif. Also: Phase 217 H/L Proximity-Fix (log-ratio), Phase 216 Fake-Distractors, Phase 215 Hyphenation, Phase 214 Crash-Fixes."
git push origin main
pause
