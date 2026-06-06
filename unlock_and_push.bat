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
git commit -m "Content: Phase 524. Pin-Bug (echte Ursache): genCapitalsPinQ (und genGeoConstQ) liefern lat/lng, das uk_pin-Scoring/Drawing liest aber targetLat/targetLng -> Distanz=NaN -> JEDE Pin-Eingabe '✗ 0 km entfernt' (Capitals-Pin komplett kaputt). Fix in der Schema-Normalisierung (nextQ): uk_pin/airport_pin bekommen targetLat/targetLng als Fallback aus lat/lng (+ ans aus subj). Deckt alle Pin-Generatoren ab (Scoring UND Kartenmarker). Verifiziert: Capitals-Pin self-dist=0, ok=true. 195/195.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
