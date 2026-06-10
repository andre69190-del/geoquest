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
git commit -m "Content: Phase 538. Feinere Regionen (Sub-Regionen-Filter): _regionOk um 'sub:<Subregion>' erweitert (nutzt COUNTRIES.sr) - alle Geo-Generatoren, die _rfilt nutzen (capital/flag/city/river/landmark/park/unesco...), respektieren den Filter automatisch. Filter pro Spiel gescopt (S._pendingFilter -> startGame setzt/raeumt S.filter). Region-Picker-Modal (21 Subregionen in 5 Gruppen) + Home-Karte 'Region ueben' -> startRegionQuiz('sub:X','capital'). i18n DE/EN/PL fuer alle Regionsnamen. Verifiziert: Osteuropa->Polen/Ukraine.., Nordafrika->Aegypten/Marokko.., Distraktoren regional.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
