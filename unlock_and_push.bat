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
git commit -m "Content: Phase 481. RUNTIME-CRASH-FIX (viele Spiele): (1) _mkHLQ war NIE definiert -> alle HL-Vergleichsspiele in Inseln/Gipfel/Klima/Ozeane crashten (ReferenceError -> lq() exhausted). _mkHLQ jetzt definiert (2-Optionen beta_hl, respektiert lowerWins/unit). (2) genKlimaPinQ las window.LAND_LATLON (const ist nicht auf window) -> jede Frage null -> klima_pin_land leer. Auf echtes LAND_LATLON umgestellt. (3) _trackCatPlay implementiert (war undefiniert, in try/catch). ZUKUNFTS-SCHUTZ: verify.py Check 21 faengt jetzt undefinierte Helfer-Funktionen ab (193/193). Beide Fehlerklassen (undefinierte *_DATA + undefinierte Funktionen) werden nun beim Build erkannt.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
