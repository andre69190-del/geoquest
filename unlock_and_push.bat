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
git commit -m "Content: Phase 522. SW-Precache verschlankt: nur noch App-Shell (GeoQuest.html/manifest/icon, ~6.1MB) wird beim Install vorab gecacht; alle data/*.json werden vom bestehenden Fetch-Handler bei Bedarf zur Laufzeit gecacht (cache.put). Hash bleibt ueber ALLE Assets inkl. Daten -> CACHE_NAME bumpt bei Datenaenderung, alte Runtime-Caches werden in activate geloescht. SW-Precache 10.1MB -> 6.1MB (Quota-Risiko weg). verify-Check 12 angepasst (Shell+Runtime-Cache statt 'alle Daten im Precache'). perf_check 0 WARN. 195/195.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
