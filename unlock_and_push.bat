@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "CHORE/SEC: Comprehensive system audit Phase 208. Fail-safe architecture (generator try/catch, null guards, state resets), memory leak fixes (clearInterval dedup, self-cancel guards), anti-cheat hardening (answerByIdx removes answers from DOM, 350ms debounce, Proxy get+set trap), i18n consistency (ws_* + mode_* keys in all 28 langs, renderWortSchmiede fully wired to t())."
git push origin main
pause
