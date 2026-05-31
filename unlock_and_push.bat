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
git commit -m "Content: Phase 323. Kultur-Balancing: wahrzeichen +40, museen +23, kunstwerke +21 — 16 unterrepräsentierte Länder (PL/CZ/HU/RO/SE/NO/FI/DK/HR/BG/BE/SK/NL/PT) ergänzt. verify: 138/138."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
