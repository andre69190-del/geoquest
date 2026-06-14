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
git commit -m "Content: Phase 572. architektur von 40 auf 55 erweitert (>=50 erreicht): 15 weltbekannte Bauwerke web-verifiziert (Koordinaten/Hoehe/Baujahr per Subagent aus Wikipedia; Hangzhou-Bay-Bruecke ohne belegte Hoehe ausgelassen - keine Schaetzung). Inkl. eindeutiger Staedte fuer arch_match_stadt. Willis Tower, The Shard, Skytree, Chrysler, Merdeka 118, Petersdom, Brandenburger Tor, Pisa, Cheops-Pyramide, Big Ben u.a.. verify: 196/196."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
