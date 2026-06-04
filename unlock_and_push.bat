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
git commit -m "Content: Phase 472. DEPLOY-FIX (PWA Stale-Cache): vercel.json hatte KEINE Cache-Control-Header. Service Worker ist cache-first -> Browser cachte alte index.html/sw.js, neue Builds kamen nie an (Symptom: alle neuen Features gleichzeitig 'weg', konsistent mit EINER alten gecachten HTML). Jetzt Cache-Control:no-cache auf /sw.js (+no-store,must-revalidate), /index.html (/play+catch-all), /manifest.json. Session-Starter um Deploy-/Cache-Falle ergaenzt. Keine gen.py-Aenderung.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
