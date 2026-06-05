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
git commit -m "Content: Phase 515. Gezielte Reparatur unloesbarer uk_match-Fragen am GENERATOR: _mkMatchQ (emob/gastro/arch/...), genTiereMatchQ und genPflanzenMatchQ nutzen fixedOpts jetzt NUR, wenn die richtige Antwort (correct.c/cor.c) darin enthalten ist; sonst werden Optionen dynamisch aus den ECHTEN Werten DIESES Modus gebaut (gleiche Art wie die Antwort) -> konsistent + loesbar. ans-nicht-in-opts von 33 auf 0 (mehrere Zufallslaeufe). Beispiel: Tempel-Ordnungen Korinthisch unter [Dorisch/Ionisch/Korinthisch/Toskanisch]. Zusammen mit lq()-Inject (Phase 514) doppelt abgesichert. verify 193/193, 0 THROW, 0 Render-Fehler.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
