@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "UI/UX: Phase 215 — Smart language-aware hyphenation for game card titles. Replaced word-break:break-word with hyphens:auto + dynamic html[lang] sync for all 28 languages. Also Phase 214: Fixed Alphabet-Sprint crash, null-generator toasts, mobile tap targets."
git push origin main
pause
