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
git commit -m "Content: Phase 567. GENAUIGKEIT: architektur 'stadt' auf 23 eindeutige Bauwerke reduziert (mehrdeutige Tunnel/Grenz-Daemme/spannende Bruecken entfernt - kein Raten). fluss_match_muendung existierte bereits (nichts doppelt gebaut). Genauigkeits-/Anti-Halluzinations-Regel im Session-Starter verankert.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
