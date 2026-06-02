@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py
if errorlevel 1 (
    echo.
    echo ABORT: verify.py FAILED - fix errors before pushing!
    pause
    exit /b 1
)
echo.
git add -A
git commit -m "Content: Phase 437. Phase 437: Datenbasis-Erweiterung. Serien 98→105 (+7), Filme 40→46 (+6), Musik 40→46 (+6), Webkultur 40→52 (+12), Wirtschaft 40→49 (+9). Serien-Enum-Fix (Sci-Fi→Sci-Fi/Mystery, Vergangenheit→Historisch). Timeline eco+web refreshed. verify: 165/165. verify: 165/165."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
