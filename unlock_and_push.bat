@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CHORE/SEC: Phase 206 System Audit -- try/catch in lq() generator loop; clr() kills SLF/WS/LH timers on exit; t() strict null-guard; wort_schmiede lang->de->en->first fallback; opt-btn CSS overflow protection; qprompt word-break hardening"
echo.
git push origin main
echo.
echo Fertig! Druecke eine Taste zum Schliessen.
pause
