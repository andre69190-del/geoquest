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
git commit -m "Content: Phase 475. (1) FIX kaputte vercel.json: war als abgeschnittene 1817-Byte-Version (invalides JSON) committet worden (Sandbox-Mount-Truncation) - haette Vercel-Deploy gebrochen. Sandbox-seitig neu geschrieben, valide (14 Routes, Cache-Control intakt). (2) _goCat robuster: Filter garantiert anwenden + Retry + harter window.scrollTo-Fallback (smooth scrollIntoView scrollte in der PWA evtl. nicht -> Sektion klappte unsichtbar weit unten auf).. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
