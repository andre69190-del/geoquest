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
git commit -m "Content: Phase 518. Options-Dedup vervollstaendigt: genDS100McQ, genCurrRealQ, genIataReverseQ erzeugten sporadisch doppelte Optionen (gleicher DS100-Code / Euro mehrfach / Stadt mit mehreren Flughaefen). Alle drei deduplizieren jetzt per Set und schliessen die Antwort aus. Bekannte 8 Kandidaten: 0/2000 dup. option_quality_test.js gruen.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
